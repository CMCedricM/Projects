#!/usr/bin/python
from googleapiclient.discovery import build

# Built in libraries
import time
import sys
import os 
import subprocess


# Track if previously run
PREV_RUN = False 

# Program Actions log 
PROGRAM_FILE = "Program-logFile.txt"
PROGRAM_LOG = open(PROGRAM_FILE, 'a')

# API Creds for yt
API_KEY_YT = None
youtube_q = None  # build('youtube', 'v3', developerKey = API_KEY_YT)

# API Keys for Twitter 

def updateLogFile(): 
    PROGRAM_LOG.write("\n----------------------------------------------------\n")
    currTime = time.localtime()
    timeData = time.strftime("%m-%d-%Y, %H:%M:%S", currTime)
    PROGRAM_LOG.write("Program running: " + timeData + "\n") 
    PROGRAM_LOG.write("----------------------------------------------------\n")

def closeLogFile():
    PROGRAM_LOG.write("\n----------------------------------------------------\n")
    currTime = time.localtime()
    timeData = time.strftime("%m-%d-%Y, %H:%M:%S", currTime)
    PROGRAM_LOG.write("Program finished: " + timeData + "\n") 
    PROGRAM_LOG.write("----------------------------------------------------\n") 
    PROGRAM_LOG.close()


def outputMsg(outputLoc, message):
    try: 
        outputLoc = int(outputLoc)
    except Exception as Err: 
        print("Error, incompatible type usage, expecting integer, can not output data: " + str(Err))
        return 

    if(outputLoc == 1):
        print(message)
    elif(outputLoc == 2):
        PROGRAM_LOG.write(str(message) + "\n")
    elif(outputLoc == 3): 
        print(message)
        PROGRAM_LOG.write(str(message) + "\n")
    else: 
        print("Call error, expecting integer from 1 - 3 to display message")
    
    
    

    


# Obtain Credentials if they exist (do for safety of API keys)
def obtainCreds(setupFileName = None):
    if(setupFileName != None and os.path.exists(setupFileName)): 
        try: 
            with open(setupFileName, 'r') as fileObj: 
                fileText = fileObj.readlines()
                global API_KEY_YT 
                API_KEY_YT = fileText[0]
                #youtube_q = build('youtube', 'v3', developerKey= API_KEY_YT)
        except Exception as Err: 
            return 
    else: 
        outputMsg(3, "API Keys Missing, program may not run properly...")
    

class YTMT:
    
    def __init__(self, args = None): 
        self.ytPlaylistID = None 
        self.ytBuild = None
        self.TAGS = []  # Will hold Tags in the playlist
        self.NEW_TAGS = [] # Will hold new videos if new videos are found
        self.args = args 
        
    class SETTINGS: # Just a little struct for now, may not need later
        def __init__(self):
            self.format = '-f m4a'
            self.playlist = '--yes-playlist'
            self.addMetadata = '--add-metadata'
        
        def set(self,format, metaData):
            self.format = "-f " + str(format)
            self.addMetadata = bool(metaData)


    def __findTag__(self, url) -> str:
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
            outputMsg(3, "There was an error: " + str(Err) + "\nTrigerring exit failure")
            closeLogFile()
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
                outputMsg(3, "There was an error: " + str(Err))
                closeLogFile()
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
                outputMsg(3, "End of playlist, saving....")
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
            outputMsg(3, "New Videos Found, updating manifest...")
            with open(ORIG_FILE, 'a') as FILE_OBJ:
                FILE_OBJ.write("\n")
                for items in self.NEW_TAGS:
                    FILE_OBJ.write(str(items) + "\n")


    # This function will create the file that holds the list of yt videos from playlist 
    # If a file is already present it will create a second log file, and see if there were any new videos added from prev run 
    def createManifest(self): 
        
        DATA_FILE_ORIG = "log.txt" 
        DATA_FILE_SECOND = "log2.txt"


        if os.path.exists(DATA_FILE_ORIG): 
            global PREV_RUN # Tell the program that it was run previously -> may affect how things run later on
            PREV_RUN = True

        if PREV_RUN == False: 
            with open(DATA_FILE_ORIG, 'w') as fileObjOne: 
                for items in self.TAGS:
                    fileObjOne.write(str(items) + "\n")
        else: 
            with open(DATA_FILE_SECOND, 'w') as fileObjTwo: 
                for items in self.TAGS: 
                    fileObjTwo.write(str(items) + "\n")
        

        if PREV_RUN: # Check for Diffs, and append diff to original storage file -> linear search, maybe implement AVL tree later
            self.__prevRan__(DATA_FILE_ORIG, DATA_FILE_SECOND)
            
            # Remove temp log (.log2.txt)
            try: 
                if os.path.exists(os.getcwd() + "/" + DATA_FILE_SECOND): 
                    os.remove(os.getcwd() + "/" + DATA_FILE_SECOND)
                    outputMsg(3, DATA_FILE_SECOND + "deleted...")
            except Exception as Err: 
                outputMsg(3, "There was an error: " + str(Err))

            
            


def debugMain(): 
    print("There's Nothing Here, LUUUL")
    
    print(sys.argv[1])
    obtainCreds(sys.argv[1])
    if API_KEY_YT == None: 
        print("Fatal Error, exiting....")
        closeLogFile()
        exit(-1)     
    print(API_KEY_YT)

    
    outputMsg(3, "Now instantiating class function...")
    youtubeDL = YTMT(sys.argv)
    youtubeDL.setup()
    outputMsg(3, "Now fetching data...")
    youtubeDL.fetchData()
    outputMsg(3, "Now creating youtube data manifest...")
    youtubeDL.createManifest()
    outputMsg(3, "Manifest Created...")


    


def main(): 
    print("There's Nothing here also, luuul")
    
    # Step 1: Obtain creds if they exist
    obtainCreds(sys.argv[1])





if __name__ == '__main__': 
    obtainCreds('keys.txt')
    updateLogFile() # Begin Logging When program starts
    debugMain() # main()
    closeLogFile() # End logging
    #main()