import os 
import subprocess

pathFiles = ".paths.txt"


def main(): 
    print("This script will setup your SERVER to use the youtube playlist monitor; this setup script WILL REQUIRE SUDO privileges.")
    print("This setup script will download dependencies needed to run the program, along with generate entry for your server's CRONTAB tool to run at designated times.")
    
    response=input("Do you agree for the above to be done on your server? (y/N)")
    if response == 'y' or response == 'Y': 
        print("You have agreeed to let this setup script use sudo privileges to configure the program.")
        setup()
    else: 
        exit(0) 

    
def setup(): 
    cmd1 =  "pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib"
    status = subprocess.call(cmd1, shell=True)
    if status != 0: 
        print("There was an error, terminating...\nError return code: " + str(status))
    
    cmd2 = "which youtube-dl"
    YOUTUBE_DL_PATH = subprocess.check_output(cmd2, shell=True, universal_newlines=True)
    if YOUTUBE_DL_PATH == None: 
        print("Could not find youtube-dl path")
        exit(-1)
    
    
    print("Path of youtube-dl is: " + str(YOUTUBE_DL_PATH)) 

    with open(pathFiles, mode='w') as file: 
        file.write(str(YOUTUBE_DL_PATH + "\n"))
    

    


    
    



        
    


if __name__ == "__main__": 
    main()