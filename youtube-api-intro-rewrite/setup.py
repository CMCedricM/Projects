import os 
import subprocess

pathFiles = ".paths.txt"


def main(): 
    print("This script will setup your SERVER to use the youtube playlist monitor, you will be required \nto append the outputted command to your CRONTAB file yourself.")
    print("Instructions to place the outputted command into crontab will be placed in the README.txt file in this program's directory.\n")
    print("This setup script will download dependencies needed to run the program, along with generate entry for your \nserver's CRONTAB tool to run at designated times.")
    
    response=input("Do you agree for the above to be done on your server? (y/N): ")
    if response == 'y' or response == 'Y': 
        print("\nYou have agreed to let this setup script download pip packages: \n\ngoogle-api-python-client\ngoogle-auth-httplib2\ngoogle-auth-oauthlib\n")
        setup()
        obtainArgs()
        scheduleCreation()
    else: 
        print("You chose not to allow this setup script to run, exiting...")
        exit(0) 

    
def setup(): 
    if os.path.exists(pathFiles): 
        ans = input("This is not the first time running setup, would you like to overwrite the old setup? (y/N): ")
        if ans == 'N' or ans == 'n': 
            print("Ok then, previous settings are still saved, setup will exit now, no files lost...")
            exit(0)
        else: 
            print("The previouis setup will be overwritten then, continuing setup program...")

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


def obtainArgs(): 

    

    arguments = input("Enter Custom Choices to run youtube-dl (i.e. -f mp4 --add-metadata): ")
    valid = False 

    while not valid: 
        playlistURL = input("Enter a playlist's full URL to constantly monitor: ")
        if playlistURL == None: 
            print("A PLAYLIST URL is required, please try again....")
        else: 
            valid = True
    
    with open(pathFiles, "w") as file: 
        file.write(str(arguments) + " " + str(playlistURL) + "\n")

def scheduleCreation(): 
    print("The next few questions will allow me to create the CRONTAB entry that you will have to copy yourelf into CRONTAB.")
    print("\nPlease note that days begin from Monday-Sunday, so MONDAY will be 1 and SUNDAY will be 7, for the day(s) of the week.\n")
    print("\nTime will be based on the 24 hour clock, so 12 am will be 0 and 10 pm will be 22\n")
    
    # Check for valid input 
    valid = False 
    while not valid: 
        getDays = input("Please enter the numbers as a space seperated list, what days would you like the program to run? (i.e. 1 5 7): ")
        
        days = [] 
        for numbers in getDays: 
            if numbers != " ": 
                try:
                    entry = int(numbers)
                except Exception as err: 
                    print("Error")
                    valid = False 
                    break 
                else: 
                    if (entry < 8) and (entry > 0): 
                        valid = True 
                        days.append(numbers)
            
    
    # Have user input the time they would like the program to run 
    valid = False
    while not valid: 
        try: 
            getHour = int(input("Enter an hour, ranging from 0-23: "))
            getMin = int(input("Enter Minute (0-59): "))
        except Exception as err: 
            print("Error, you did not enter a valid whole number, try again...")
        else: 
            if (getHour < 0) or (getHour > 23): 
                print("Error, you did not enter a valid hour, please try again....")
            elif (getMin < 0) or (getMin > 59): 
                print("Error, you did not enter a valid minute, please try again...")
            else: 
                valid = True 
        
    
    # Format Days 
    finalDays = ""
    if len(days) != 1: 
        for i in range(len(days)):
            finalDays += days[i]
            if i + 1 < len(days): 
                finalDays += ","

    else: 
        finalDays = days[0]

    if not os.path.exists("Vid-manifest.txt"): 
        print("The download program must run, before setup can be complete, if you do not run this program now, then it may not work correctly. ")
        ans = input("\n Run the program now? (Y/n): ")
        if ans == 'Y' or ans == 'y': 
            print("Will run program...")
        else: 
            print("Will not run program, undoing installation....")
            os.remove(pathFiles)
            exit(-1)
        
        cmd = "python3 " + os.getcwd() + "/run.py"
        ret = os.system(cmd)

        if ret != 0: 
            print("Fatal error, this program was not able to run, exiting...")
            os.remove(pathFiles)
            exit(-1)
        else: 
            print("Program Execution Successful, now making your schedule entry...")
        

    print("\n\nCrontab entry is: " + str (getMin) + " " + str(getHour) + " * * " +  str(finalDays) + " " + str(os.getcwd()) + "/run.py\n"  )




if __name__ == "__main__": 
    main()