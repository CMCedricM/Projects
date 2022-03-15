#!/bin/python3 
import os, sys, subprocess
import json, time, pymongo
import traceback
from pymongo import MongoClient
import googleapiclient.discovery as gAPI
import shutil


from Resources.ytSetup import yt_Program_Setup
from Resources.removeTags import TagRemover
# Debug Var     
_Debug_Active = False 
_Output_Loc = 2
if len(sys.argv) > 1:
    if sys.argv[1] == "--debug":
        _Debug_Active = True 
        _Output_Loc = 3

# Log Var     
TIME_FORMAT ='%H:%M:%S'
        
class yt_App: 
    
    
    def __init__(self):
        # Setup DB links and API 
        self._ProgramSetup = yt_Program_Setup()
        # Program Constants
        # Status Codes 
        self._StatusCodes = ['Completed', 'Failed', 'Downloading', 'Deleted']
        # General Setup 
        self._API_KEY, self._DB, self._COLLECTION, self._YT_Client = None, None, None, None 
        self._LOG = None 
        self._Settings = None 
        
        # Program User
        self._User = None 
        
        # Video Prefix Constant
        self._YT_Begin = "https://youtu.be/" # All youtube videos, when shared, have this url shortcut attached to the tag
        
        self._PlaylistURL = None 
        self._SaveVideoDirectory = None 
        self._TempVidDirectory = None 

        # Database Records
        self._Vids, self._Cntr, self._oldVids, self._compareVids = list(), 0, dict(), list()
        
        # Variables to Hold Upload DAta
        # { date: { videoURL : [] } }
        self._VidDict = dict() 
        self._CurrDate = time.strftime('%Y-%d-%m')
        
        # Tag removing program
        self._TagRemoveProgram = None 
        
        self.ErrorCnt = 0 
        
        

    def setupProgram(self): 
        # Setup Program
        self._ProgramSetup.setup()
        # Assign Necessary Connection Values
        self._API_KEY, self._YT_Client, self._LOG = self._ProgramSetup.getKey(), self._ProgramSetup.getYTRef(), self._ProgramSetup.getLogRef()
        self._DB, self._COLLECTION = self._ProgramSetup.getDBRef()
        self._Settings = (self._ProgramSetup.getSettings())
        try: 
            if self._Settings is not None: 
                self._PlaylistURL = self._Settings['playlistID']
                self._SaveVideoDirectory = self._Settings['saveDirectory']
                self._User = self._Settings['user']
        except Exception as err: 
            self._LOG.output(3, f"{time.strftime(TIME_FORMAT)} ---> There was an error retrieving data from settings file : \n{err}\n")
            exit(-1)
        
    
      
    # This will create a list of video tags in the playlist
    def queryYT(self): 
        if self._PlaylistURL is None: 
            self._LOG.output(3, f"{time.strftime(TIME_FORMAT)} ---> Error: No Playlist URL Specified")
            exit(-1)
        
        next_Page_Token, yt_Response = None, None
        # Output A Status Update to Log File
        self._LOG.output(_Output_Loc, f"{time.strftime(TIME_FORMAT)} ---> Attempting YT Query...")
        
        while True: 
            try:  
                # Get the Response 
                yt_Response = self._YT_Client.playlistItems().list(
                    part = 'contentDetails',
                    playlistId = self._PlaylistURL, 
                    pageToken = next_Page_Token  
                ).execute()
                  
                # Loop Through the Items in the Query
                for tags in yt_Response['items']: 
                    self._Vids.append(tags['contentDetails']['videoId'])
                    self._Cntr += 1      
                    
            except Exception as err: 
                self._LOG.output(_Output_Loc, f"{time.strftime(TIME_FORMAT)} ---> \'queryYT\' had an Error: {err}\n")
                exit(-1)
            
                
            # Check if there is another page, otherwise break out
            try: 
                next_Page_Token = yt_Response['nextPageToken']
            except Exception as err:
                break
        
        # Report Query Was Successful
        self._LOG.output(_Output_Loc, f"{time.strftime(TIME_FORMAT)} ---> YT Query Executed Successfully!")
    
        
        if _Debug_Active:
            # Debug Print
            for i, items in enumerate(self._Vids): 
                print(f"{i}:\t{items}")
            
            print(len(self._Vids))
    
    # Create Fields
    def saveToDict(self, videoID, status=None): 
        if not self._VidDict: 
            self._VidDict.update({"User" : self._User, "Date": self._CurrDate, "Video" : []})
        
        self._VidDict['Video'].append({'videoTag' : videoID, 'status' : status})
    
    
    def uploadData(self): 
        try: 
            self._COLLECTION.insert_one(self._VidDict)
        except Exception as err: 
            self._LOG.output(_Output_Loc, f"{time.strftime(TIME_FORMAT)} ---> There was an error uploading to the database ---> Error: \n{err}\n")
            self.ErrorCnt += 1 
    
    def checkForPastVids(self): 
        # Check if we want to skip the past video check
        if len(sys.argv) > 2: 
            if sys.argv[2] == "--fresh": 
                return 
            
        try: 
            # Example Query from prev program:
            # self._patientCollection.find({'$and' : [{'PatientID' : ptID}, {'PatientName' : {'$regex': name, '$options' : 'i'}}]})
            self._oldVids = self._COLLECTION.find({'User' : self._User}).sort("Date", pymongo.DESCENDING)[0]
        except Exception as err: 
            self._LOG.output(_Output_Loc, f"{time.strftime(TIME_FORMAT)} ---> There was an error with grabbing past logs --> Error: \n{err}\n")
            self._LOG.output(_Output_Loc, f"---> Traceback: {traceback.format_exc()}")
            self.ErrorCnt += 1
        else: 
            tempArr = list()
            # Now Grab All The Video Ids and save it temporarily, then replace old_Vids dict with this new array
            for data in self._oldVids['Video']: 
                tempArr.append(data)
            self._oldVids = tempArr 
        
    
        
    def checkPrev(self, videoId) -> int: 
        if len(list(self._oldVids)) == 0: 
            return 0 
        
        for data in self._oldVids: 
            # If the video matches and it was previously downloaded succesfully, then return 1, indicating there is no need
            # to download it again
            if videoId == data['videoTag'] and data['status'] == self._StatusCodes[0]: 
                return 1 
        
        return 0 
            
            
    
    
    def download(self): 
        
        self._TempVidDirectory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Videos")
        if not os.path.exists(self._TempVidDirectory): 
            os.mkdir(self._TempVidDirectory)
            
        # Now Change the Directory since I cant modify the output of yt-dlp 
        os.chdir(self._TempVidDirectory)
            
        # Now Loop and download vids
        for i, videoTag in enumerate(self._Vids): 
            statusCode = self._StatusCodes[2]
            try: 
                if self.checkPrev(videoTag) == 0: 
                    subprocess.run(['yt-dlp', '-fm4a', "--embed-thumbnail", "--embed-metadata", (self._YT_Begin + videoTag)], check=True)
            except Exception as err: 
                self._LOG.output(_Output_Loc, f"{time.strftime(TIME_FORMAT)} ---> Video {i} : {videoTag} ---> error: \n{err}\n")
                statusCode = self._StatusCodes[1]
                self.ErrorCnt += 1 
            # Check if the video failed to download or not
            if statusCode != "Failed": 
                statusCode = self._StatusCodes[0]
            # Save the video to the dictionary
            self.saveToDict(videoTag, statusCode)
      
      
    def cleanMusicTags(self): 
        self._TagRemoveProgram = TagRemover(self._TempVidDirectory, '[')
        self._TagRemoveProgram.run()
        self._LOG.output(_Output_Loc, f"{time.strftime(TIME_FORMAT)} ---> All Tags Cleaned!")
    
    
    def moveMusic(self): 
        if not os.path.exists(self._SaveVideoDirectory): 
            self._LOG.output(_Output_Loc, f"{time.strftime(TIME_FORMAT)} ---> Error: {self._SaveVideoDirectory} Not Found")
            self.ErrorCnt += 1
            return 
        
        for root, _, files in os.walk(self._TempVidDirectory): 
            for aFile in files: 
                shutil.move(os.path.join(root,aFile), self._SaveVideoDirectory)
        self._LOG.output(_Output_Loc, f"{time.strftime(TIME_FORMAT)} ---> All Downloaded Videos Have Been Moved!")
        
            
            
    def runTime(self): 
        
        # Main Program Run 
        self.setupProgram()
        self.checkForPastVids()
        self.queryYT()
        self.download()
        self.uploadData()
        # Do The Clean Up 
        self.cleanMusicTags()
        self.moveMusic()
        
        # Output End Message
        if self.ErrorCnt > 0: 
            # Output the Program Was Successfully Ran but with errors
            self._LOG.output(_Output_Loc,f"{time.strftime(TIME_FORMAT)} ---> Program Executed With Errors!\nError Count: {self.ErrorCnt}")
        else: 
            # Output the Program Was Successfully Ran 
            self._LOG.output(_Output_Loc,f"{time.strftime(TIME_FORMAT)} ---> Program Execution Successful!")
       
        # End the Program 
        self._ProgramSetup.closeProgram()
        
        
        
     
if __name__ == "__main__": 
    main=yt_App()
    main.runTime()
        