import os 


def main(): 

    canRun = False
    if not os.path.exists("Vid-manifest.txt" ):
        print("This is the first time running this program, therefore an initial run must be made.")
        ans = input("Can the program run now?(y/N): ")
        if ans == 'y' or ans == 'Y': 
            canRun = True 
        else: 
            print("Setup failed, please try again, please not this program must run initially before it can be placed into CRONTAB...")
            exit(-1)
    else: 
        canRun = True 
        


    cmd  = "python3 ytdl_watch.py keys.txt"
    with open(".paths.txt", "r") as file: 
        arguments = file.read()
    cmd += " " + str(arguments)


    if canRun: 
        ret = os.system(cmd)
        if ret != 0: 
            print("There was a fata error, please view log file ytdl-log.txt for more information..")
            exit(-1)

    

    
    

if __name__ == "__main__": 
    main()