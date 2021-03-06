#!/usr/bin/python
#from typing import NewType, Sequence
from googleapiclient.discovery import build
from library import Logging as LOGGING
# Built in libraries
import sys
import os 
import subprocess
import time


# Track if previously run
PREV_RUN = False 

# API Creds for yt
API_KEY_YT = None

class YTMT:
    
    def __init__(self, args = None): 
        self.log = LOGGING.LOGGING(os.path.join(os.path.dirname(__file__),"ytdl-log.txt"))
        self.ytPlaylistID = None 
        self.ytBuild = None
        self.TAGS = []  # Will hold Tags in the playlist
        self.NEW_TAGS = [] # Will hold new videos if new videos are found
        self.args = args 
        
   
    
    # Obtain Credentials if they exist (do for safety of API keys)
    def obtainCreds(self,setupFileName = None):
        #print(os.path.join(os.getcwd(), setupFileName))
        if(setupFileName != None and os.path.exists(os.path.join(os.path.dirname(__file__),setupFileName))): 
            setupFileName = os.path.join(os.path.dirname(__file__),setupFileName)
            try: 
                with open(setupFileName, 'r') as fileObj: 
                    fileText = fileObj.readlines()
                    global API_KEY_YT 
                    API_KEY_YT = fileText[0]
                    #youtube_q = build('youtube', 'v3', developerKey= API_KEY_YT)
            except Exception as Err: 
                print("Error Usage: python3 main.py <API_KEY_FILE_NAME> <list of args> <youtube playlist url> ")
                exit(-1) 
        else: 
            self.log.output(3, "API Keys Missing, program may not run properly...")
        
        return API_KEY_YT


    def __findTag__(self, url):
        tag = ""
        record = False 
        
        for aChar in url: 
            if aChar == '=':
                record = True 
            elif record == True: 
                tag += aChar 

        return tag

                
    def setup(self): 
    
        try: 
            self.ytBuild = build('youtube', 'v3', developerKey= API_KEY_YT) # uncomment when ready to run program
            self.ytPlaylistID = self.args[len(self.args) - 1] # Obtain the playlist url or id, should always be last arg
        except Exception as Err: 
            self.log.output(3, "There was an error: " + str(Err) + "\nTrigerring exit failure")
            self.log.closeFile()
            exit(-1)
        # Check if user gave full url or just a tag
        fullURL = False
        for chars in self.ytPlaylistID:
            if(chars == '/' or chars == '\\'): 
                fullURL = True
                break
        
        if fullURL == True: # If it is a tag, then i need to append the standard url 
            self.ytPlaylistID = self.__findTag__(self.ytPlaylistID)
    

    def fetchData(self): 
        
        nxtPageToken = None 

        while True: 
            try:
                ytResponse = self.ytBuild.playlistItems().list(
                    part = 'contentDetails', 
                    playlistId = self.ytPlaylistID, 
                    pageToken = nxtPageToken
                ).execute()
            except Exception as Err: 
                self.log.output(3, "There was an error: " + str(Err))
                self.log.closeFile()
                exit(-1)
            
            # Obtain videos, add youtu.be shortner and save to an array
            for tags in ytResponse['items']: 
                aTag = tags['contentDetails']['videoId']
                self.TAGS.append("https://youtu.be/" + aTag)

            # Continue to next page, if one exists
            try: 
                # Grab the next page token 
                nxtPageToken = ytResponse['nextPageToken']
            except Exception as Err: # If a next page token was not found, it is the end of the playlist
                self.log.output(3, "End of playlist, saving....")
                return 
    

    # Helper function for YTMT::createManifest() function
    def __prevRan__(self, ORIG_FILE, SECOND_FILE):
        dataFromOrig = ''
        dataFromNew = ''
        # Save data into main memory
        with open(ORIG_FILE, 'r') as fileObjOne: 
            dataFromOrig = fileObjOne.readlines()
        with open(SECOND_FILE, 'r') as fileObjTwo: 
            dataFromNew = fileObjTwo.readlines()
        
        # Create an array that will contain new videos, if they exist -> already created in constructor, just for readability
        self.NEW_TAGS = []
        # We can assume that the second file should be longer, if new additions were made, so search based off second log file
        for aLine in dataFromNew: 
            currWord = aLine
            found = False 
            for checkLines in dataFromOrig: 
                if checkLines == currWord: 
                    found = True 
                    break 
            if not found:
                self.NEW_TAGS.append(currWord)
        
        # If new data was found then append to original file 
        if len(self.NEW_TAGS) != 0: 
            self.log.output(3, "New Videos Found, updating manifest...")
            with open(ORIG_FILE, 'a') as FILE_OBJ:
                FILE_OBJ.write("\n")
                for items in self.NEW_TAGS:
                    FILE_OBJ.write(str(items) + "\n")


    # This function will create the file that holds the list of yt videos from playlist 
    # If a file is already present it will create a second log file, and see if there were any new videos added from prev run 
    def createManifest(self): 
        
        DATA_FILE_ORIG = os.path.join(os.path.dirname(__file__),"Vid-manifest.txt")
        DATA_FILE_SECOND = os.path.join(os.path.dirname(__file__),"Vid-manifest2.txt") 


        if os.path.exists(DATA_FILE_ORIG): 
            global PREV_RUN # Tell the program that it was run previously -> may affect how things run later on
            PREV_RUN = True
            self.log.output(3, "This program was previously ran, now creating secondary file for comparison....")

        if PREV_RUN == False: 
            with open(DATA_FILE_ORIG, 'w') as fileObjOne: 
                for items in self.TAGS:
                    fileObjOne.write(str(items) + "\n")
            self.log.output(3, "New Manifest Created...")
        else: 
            with open(DATA_FILE_SECOND, 'w') as fileObjTwo: 
                for items in self.TAGS: 
                    fileObjTwo.write(str(items) + "\n")
            
        

        if PREV_RUN: # Check for Diffs, and append diff to original storage file -> linear search, maybe implement AVL tree later
            self.__prevRan__(DATA_FILE_ORIG, DATA_FILE_SECOND)
            
            # Remove temp log (.log2.txt)
            try: 
                if os.path.exists(DATA_FILE_SECOND): 
                    os.remove(DATA_FILE_SECOND)
                    self.log.output(3, DATA_FILE_SECOND + " deleted...")
            except Exception as Err: 
                self.log.output(3, "There was an error: " + str(Err))
        else: 
            self.NEW_TAGS = self.TAGS
        
        self.log.output(3,"Diff check complete")
        
          
    def download(self): 
        cntr = 0 
        self.log.output(3,"Setting Up Download")     
        # Set the youtube-dl path now
        YOUTUBE_DL_PATH = "/snap/bin/youtube-dl" #subprocess.check_output("which youtube-dl", shell=True, universal_newlines=True)
        '''
        if YOUTUBE_DL_PATH == None:
            print("Youtube-dl path not found error")
        else: 
            YOUTUBE_DL_PATH=str(YOUTUBE_DL_PATH).strip()
        '''

        # Debug path print, remove when finished 
        self.log.output(3,"Path of youtube-dl is: " + str(YOUTUBE_DL_PATH)) 
        
        # Append the arguments to the youtube-dl path
        original = YOUTUBE_DL_PATH + " "
        for i in range(len(self.args) - 1): 
            if cntr > 1: 
                original += self.args[i] + " "
            else: 
                cntr += 1
        
        
        # Debug print the template for downloading 
        print(original)

        # Log the amount of data found
        self.log.output(2, "New Items Count = " + str(len(self.NEW_TAGS)))
        
        print("New Itmes Count = " + str(len(self.NEW_TAGS)))
        # Give the viewer time to see the new items found count
        time.sleep(2.5)

        tracker = 0 # Helps with visual progress tracking
        for tags in self.NEW_TAGS: 
            tracker += 1
            cmd = original + " " + str(tags)
            print("Downloading Item Number: " + str(tracker) + " of " + str(len(self.NEW_TAGS)))
            print(cmd)
            run = subprocess.call(cmd, shell=True)
            if run != 0: 
                self.log.output(3, "There was an error downloading item tag: " + str(tags) + "\nError Code ---> " + str(run))
            
        
        playlistFolder = os.path.join(os.path.dirname(__file__),"youtube-dl-playlist")
        if not os.path.exists(playlistFolder): 
           print("Making Playlist Folder")
           os.mkdir(playlistFolder)
        
        # Now move all downloaded music to the youtube-dl-playlist folder 
        cmd2 = "mv *.m4a " + playlistFolder
        subprocess.call(cmd2, shell=True)

        # End Program 
        self.log.closeFile()
        

    
def main(): 
    print("Program Beginning, please wait...")
   # if sys.argv[1] != os.path.join(os.path.dirname(__file__),"keys.txt"): 
    #    print("Error, No API KEYS Given, program cannot run properly")
        
    
    # Instantiate Class YTMT
    youtubeDL = YTMT(sys.argv)

    # Obtain API KEY
    key = youtubeDL.obtainCreds(sys.argv[1])
    
    # Run Setup 
    youtubeDL.setup()
    # Fetch All Videos from Playlist
    youtubeDL.fetchData()
    # Create long-term storage file to hold fetched id's 
    youtubeDL.createManifest()
    # Begin Downloading Videos
    print("Now Downloading, please wait....")
    youtubeDL.download()



if __name__ == '__main__': 
    main()
    #debugMain() # main()
    
