//Created By: Cedric Men on 7/26/2020


#include <iostream> 
#include <iomanip>
#include <fstream> //Will be used for logging 
#include <cctype>   //Parses the extension into all lower case to compare
#include <cstdlib> //Used for Rand in case duplicate file name
#include <experimental/filesystem>

namespace fs = std::experimental::filesystem; //define the namesapce, to shorten typing

int isProper(const fs::path &src); //Pre-definition to be used in listall function

//Create a Function to list All Files and Directories
int listAll(fs::path startPath){

    int imgCnt = 0; 
    std::ofstream outData; 
    std::string fileNameN = "filesList.txt"; 

    outData.open(fileNameN); 


    for(auto &p : fs::recursive_directory_iterator(startPath)){
        
        fs::path current = p.path(); 
        int checker = isProper(current); 
         if(checker == 1 or checker == 2){
            imgCnt++; 
            outData<<p.path()<<std::endl<<std::endl; 
        } 
    }

    outData.close(); 

    return imgCnt; 
}


//Create a Function to see if the current item is a duplicate in destination folder
bool isDuplicate(fs::path &src, fs::path &dest){


    for(auto &p : fs::directory_iterator(dest)){
        fs::path comp = p.path(); 
        if(src.filename() == comp.filename()){
            return true; 
        }
    }

    return false; 
}

//This function will lower case the extension and then determine if it is an image file
int isProper(const fs::path &src){


    std::string extensionH = src.extension().string(); 
    std::string cleanedExt = ""; 

    for(int i = 0; i < extensionH.size(); i++){
        if(i == 0){
            cleanedExt = tolower(extensionH[i]); 
        }else{
            cleanedExt += tolower(extensionH[i]);
        }
    }

    if(cleanedExt == ".jpg" or cleanedExt == ".png" or cleanedExt == ".heic" or cleanedExt == ".jpeg" or cleanedExt == ".gif"){
        return 1; 
    }else if(cleanedExt == ".mov" or cleanedExt == ".mp4" or cleanedExt == ".mpeg4" or cleanedExt == ".m4v"){
        return 2; 
    }

    return -5; 
    
}


//#define copyFile
int extractPics(const fs::path &src, fs::path &dest){
 
    int imgCnt = 0; 

    for(auto &file: fs::recursive_directory_iterator(src)){


        fs::path currentFile = file.path(); 
        std::string newFName = "";
        int checker2 = isProper(currentFile); 
        if(checker2 == 1){
            if(isDuplicate(currentFile, dest)){
                newFName = dest.string() + std::to_string(rand()) + file.path().extension().string();
                //std::cout<<newFName<<std::endl;
                //std::cout<<file.path()<<std::endl;
                currentFile = newFName; 
            }else{//Since there is not duplicate, I will keep the name but still move 
                newFName = dest.string() + file.path().stem().string() +  file.path().extension().string();
            }

            //Now Copy data over
            try{
                fs::copy(file, newFName);
                imgCnt++; //end of if the file is an image
            }catch(fs::filesystem_error &e){
                std::cout<<"Error: "<<e.what()<<std::endl;
            }
            //fs::rename(file, newFName); 

        } //end of overall if

    }//end of for loop
    
    return imgCnt; 

}


int extractVids(const fs::path &src, fs::path &dest){

    int vidCntR = 0; 


    for(auto &file: fs::recursive_directory_iterator(src)){

        fs::path currentFile = file.path(); 
        std::string newFName = "";
        int checker2 = isProper(currentFile); 
        if(checker2 == 2){
            if(isDuplicate(currentFile, dest)){
                newFName = dest.string() + std::to_string(rand()) + file.path().extension().string();
                //std::cout<<newFName<<std::endl;
                //std::cout<<file.path()<<std::endl;
                currentFile = newFName; 
            }else{//Since there is not duplicate, I will keep the name but still move 
                newFName = dest.string() + file.path().stem().string() +  file.path().extension().string();
            }

            //Now Copy data over
             //Now Copy data over
            try{
                fs::copy(file, newFName);
                vidCntR++; 
            }catch(fs::filesystem_error &e){
                std::cout<<"Error: "<<e.what()<<std::endl;
            }
            //fs::rename(file, newFName); 

        } //end of overall if

    }//end of for loop

    return vidCntR; 
}



int main(int argc, char **argv){
    
    //Initial Path Variables
    fs::path parentDirectory = fs::current_path(); 
    fs::path desiredDirectory = fs::current_path(); 
    //Modifiable pathing
    std::string directoryNameStr = fs::current_path().string(); 
    std::string directoryToExplore = " "; 
    //Counters
    int origImgCnt = 0; 
    int picCnt = 0; 
    int vidCnt = 0; 

    //Start Message: 
    std::cout<<std::endl;
    std::cout<<"Program Beginning, Current Directory: "<<parentDirectory<<std::endl<<std::endl; 

    //Get the Directory To Start Exploring
    bool badAnswer = true; 
    while(badAnswer){
        std::cout<<"Enter the Desired Folder To Search: "; 
        std::cin>>directoryToExplore; 
        //Append
        directoryNameStr += "/" + directoryToExplore;
        //Convert to a Path Type
        desiredDirectory = directoryNameStr; 
        //Check if Directory Exists
        std::cout<<"Directory Name Explore = "<<directoryNameStr<<std::endl<<std::endl;; 
        if(fs::exists(desiredDirectory)){
            break; 
        }else{
            std::cout<<"NO SUCH DIRECTORY"<<std::endl; 
            directoryNameStr = fs::current_path();
        }
    }
    //End Check for explore folder
    //This will be source folder
    const fs::path srcFolder = desiredDirectory; 

    //Re-init
    directoryNameStr = fs::current_path(); 
    //Begin Check for Dest Folder
    badAnswer = true; 
    std::string directOut = " "; 
    while(badAnswer){
        std::cout<<"Enter Destination Folder: "; 
        std::cin>>directOut; 
        //Append 
        directoryNameStr += "/" + directOut; 
        //Check if Directory Exist
        if(fs::exists(directoryNameStr)){
            directoryNameStr += "/"; //needed to copy data over and ensure that the directory does not merge with file name
            std::cout<<"Destination Directory =  "<<directoryNameStr<<std::endl<<std::endl; 
            break;
        }else{
            std::cout<<"NO SUCH DIRECTORY"<<std::endl; 
            directoryNameStr = fs::current_path(); 
        }
        
    }

    //This will hold the destFolder
     fs::path destFolder = directoryNameStr;    //Note that the folder is the parent directory with a / included
    //End Of Checks 




    //Now For Actual Program 
    srand(time(NULL)); 

    //output status message
    std::cout<<"Counting Amount of Images/Videos In The Directory...."<<std::endl; 
    //First Find cnt of images
    origImgCnt = listAll(srcFolder); 

    //Run the Program that will copy and return total images copied
    std::cout<<"Counting Is Finished, continuing..."<<std::endl<<std::endl; 

    bool badAnswerP = true; 

    do{
        std::cout<<std::left<<std::setw(30)<<std::setfill('-')<<"--"<<std::endl;
        std::cout<<"Options: "<<std::endl; 
        std::cout<<"I = Images Only"<<std::endl; 
        std::cout<<"M = Videos Only"<<std::endl; 
        std::cout<<"B = Images and Videos"<<std::endl; 
        std::cout<<"Q = Quit"<<std::endl<<std::endl; 
        std::cout<<"What Would You Like To Extract (I/M/B/Q): "; 
        char ans = ' ';
        char lowerAns = ' ';
        std::cin>>ans; 
        lowerAns = tolower(ans);  
        if(std::cin.fail()){
            std::cin.clear(); 
            std::cin.ignore(100, '\n');
            ans = 'd'; 
        }
        std::cout<<std::left<<std::setw(30)<<std::setfill('-')<<"--"<<std::endl;
        switch(lowerAns){

            case 'i':{
                std::cout<<"Processing and Copying, Please Wait..."<<std::endl; 
                picCnt = extractPics(srcFolder, destFolder); 
                badAnswerP = false; 
                break; 
            }case 'm':{
                std::cout<<"Processing and Copying, Please Wait..."<<std::endl; 
                vidCnt = extractVids(srcFolder, destFolder); 
                badAnswerP = false; 
                break; 
            }case 'b':{
                std::cout<<"Copying Images, Please Wait..."<<std::endl; 
                picCnt = extractPics(srcFolder, destFolder); 
                std::cout<<"Image Copying Complete"<<std::endl; 
                std::cout<<"Now Extracting Videos, Please Wait..."<<std::endl; 
                vidCnt = extractVids(srcFolder, destFolder);
                badAnswerP = false; 
                break;
            }case 'q':{
                std::cout<<"Quiting..."<<std::endl; 
                exit(0); 
            }

            default:{
                std::cout<<"Invalid Answer"<<std::endl; 
            }
        }
    }while(badAnswerP);



    //End of Program
    std::cout<<std::endl; 
    std::cout<<std::left<<std::setw(30)<<std::setfill('-')<<"--"<<std::endl;
    std::cout<<"Statistics: "<<std::endl; 
    std::cout<<std::left<<std::setw(30)<<std::setfill('-')<<"--"<<std::endl;
    std::cout<<"Original Image/Video Count = "<<origImgCnt<<std::endl; 
    std::cout<<"Images Copied = "<<picCnt<<std::endl; 
    std::cout<<"Videos Copied = "<<vidCnt<<std::endl; 

    return 0; 


}