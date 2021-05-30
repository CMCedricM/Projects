from copy import Error
from googleapiclient.discovery import _PAGE_TOKEN_NAMES, build
import os


# This is an introduction to the youtube-api, note that this program will only print
# out 5 video links

# Authentication 
API_KEY = 'AIzaSyCD1OfSfCj1WHqIZhNoqHWzifv-7bmtXHE'
youtube = build('youtube', 'v3', developerKey=API_KEY)



def main():

    #idNum = 'UCCezIgC97PvUuR4_gbFUs5g' # example channel
    idNum = 'UC0HIYWFalGowcdK_TNT63zg' # my channel
    playId = 'PLwnRU_LD0h-u-phV84fOH-VK-Hy6tI3I5'
    #playId = 'PLwnRU_LD0h-sGHhIbts1yZdNDpMaK8Sc8'
    
    # Initial Data Fetch
    playlistHolder = youtube.playlistItems().list(
        part='contentDetails',
        playlistId= playId

    ).execute()

    #print(playlistHolder) 
    print("Now Listing First 5 Videos: ")
    for video in playlistHolder['items']:
        tag = video['contentDetails']['videoId']
        print(tag)

    # print(playlistHolder)

    # end initial capture

    ####################################################

    # Begin a while true loop 
    # Now try to wrap this all in a while true loop, and exit when no next_token obtained
    try: 
        next_token = playlistHolder['nextPageToken']
    except: 
        print("End of playlist, exiting now...")
        exit(0)
    
    # Debug

    print(playlistHolder)

    print("\nNext Page Token Code: " , next_token)
    # End initial capture

    playlistHolder = youtube.playlistItems().list(
        part='contentDetails',
        playlistId= playId,
        pageToken = next_token

    ).execute()

    print("Now Listing Next 5 Videos: ")
    for video in playlistHolder['items']:
        tag = video['contentDetails']['videoId']
        print(tag)
    print(next_token)

    # end of loop
    
        


# Example url 
# youtu.be/m7c1sOvI_2M -> last portion can be found from any of the urls
# use tokenizing to seperate


    

    



if __name__=="__main__":
    main()


