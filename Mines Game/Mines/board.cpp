/*
    Coded By: Cedric Men 
    Date: JUL 16, 2020 
*/

#include "board.h"
#include <cstdlib> 

Board::Board(){
    height = 0; 
    width = 0; 
    mineArr = NULL; 
    mineCount = 0; 
    minesRevealed = 0; 
    spaces = 0; 
}

void Board::deleteArr(){

    for(int i = 0; i < height; i++){
        delete [] mineArr[i]; 
    }

    delete [] mineArr; 
    mineArr = NULL; 
}

Board::~Board(){
    if(mineArr != NULL){deleteArr();}
}

//Now to the Actual Functions
void Board::setDimensions(int h_in, int w_in){
    height = h_in; 
    width = w_in; 
}


void Board::allocateArr(){
    
    //Allocate the array 
    mineArr = new Mines *[height];
    for(int i = 0; i < height; i++){
        mineArr[i] = new Mines[width];
    }
    return;
    //Initilize the array 
    for(int i = 0; i < height; i++){
        for(int j = 0; j < width; i++){
            mineArr[i][j].charHolder = ' '; 
            mineArr[i][j].isFlagged = false; 
            mineArr[i][j].isMine = false; 
            mineArr[i][j].isRevealed = false; 
        }
    }

}


void Board::assignMines(){
    
    mineCount = rand() % height; 
    if(mineCount == 0){
        mineCount = 1;
    }

    for(int i = 0; i < mineCount; i++){
        int x_mine = rand() % height; 
        int y_mine = rand() % width;
        mineArr[x_mine][y_mine].charHolder = '*';
        mineArr[x_mine][y_mine].isMine = true; 
    }

    spaces = (height * width) - mineCount; 
}


void Board::printBoardInit(){

    std::cout<<std::endl;
    std::cout<<"Mine Count: "<<mineCount<<std::endl; 
    std::cout<<"    ";
    for(int i = 0; i < width; i++){
        std::cout<<std::setw(widthManip)<<std::left<<std::setfill(' ')<<i; 
    }
    std::cout<<std::endl; 
    for(int i = 0; i < height; i++){
         std::cout<<std::setw(widthManip - 2)<<std::left<<std::setfill(' ')<<i<<" "; 
        for(int j = 0; j < width; j++){
            std::cout<<std::setw(widthManip)<<std::left<<std::setfill(' ')<<"|---"; 
        }
        std::cout<<"|"<<std::endl<<std::endl; 
    }

    std::cout<<std::endl; 
}


void Board::revealBoard(){

    std::cout<<"    ";
    for(int i = 0; i < width; i++){
        std::cout<<std::setw(widthManip)<<std::left<<std::setfill(' ')<<i; 
    }
    std::cout<<std::endl; 

    char temp = ' ';
    for(int i = 0; i < height; i++){
        std::cout<<std::setw(widthManip - 2)<<std::left<<std::setfill(' ')<<i<<" ";
        for(int j = 0; j < width; j++){
            temp = mineArr[i][j].charHolder; 
            if(mineArr[i][j].isMine == false){
                std::cout<<"|   "; 
            }else{
                std::cout<<"| "<<mineArr[i][j].charHolder<<" ";  
            }
        }
        std::cout<<"|"<<std::endl<<std::endl; 
    }
}


void Board::refreshBoard(){

    char temp = ' '; 
    std::cout<<std::endl; 
    std::cout<<"    ";
    for(int i = 0; i < width; i++){
        std::cout<<std::setw(widthManip)<<std::left<<std::setfill(' ')<<i; 
    }
    std::cout<<std::endl; 

    for(int i = 0; i < height; i++){
        std::cout<<std::setw(widthManip - 2)<<std::left<<std::setfill(' ')<<i<<" ";
        for(int j = 0; j < width; j++){
            std::cout<<"|"; 
            temp = mineArr[i][j].charHolder; 
            if(mineArr[i][j].isRevealed == true){
                std::cout<<std::setw(4)<<temp; 
            }else if(mineArr[i][j].isFlagged == true){
                std::cout<<" F "; 
            }else{std::cout<<"---";}
        }
        std::cout<<"|"<<std::endl<<std::endl; 
    }

    std::cout<<std::endl; 
}


int Board::cntMinesRem(){

    
    int minesLeft = 0; 
    for(int i = 0; i < height; i++){
        for(int j = 0; j < width; j++){
            if(mineArr[i][j].isRevealed == false and mineArr[i][j].isMine == true){
                minesLeft++; 
            }
        }
    }

    return minesLeft;
}


/*
This function will go to the location the user inputs
and then attempts to see if there was a mine there, and if 
there is the game is over and a return code indicating the 
end would be returned. 

Codes: 
-5 : Indicates Error
3  : Indicates game is over
0  : Indicates that the location was a space and will reveal
    the areas around


*/
int Board::gotoLocation(int x, int y){

    if(mineArr == NULL){
        system("clear"); 
        std::cout<<"Fatal Error"<<std::endl; 
        return -5; 
    }

    if(mineArr[x][y].isMine == true){
        return 3; 
    }

    return 0; 

}


void Board::revealElem(int x, int y){
    mineArr[x][y].isRevealed = true; 
    revealSurroundingCnt(x,y); 
}

void Board::flagElem(int x, int y){
    mineArr[x][y].isFlagged = true; 
}

int Board::revealSurroundingCnt(int x, int y){

    //Check the diagnoals and the above and below
    int surroundingMines = 0; 

    //To Find the right point, just do y + 1, x = 0 
    if(y + 1 < width){
        if(mineArr[x][y + 1].isMine == true){
            surroundingMines++; 
        }
    }
    //To find the left point do y - 1
    if(y - 1 > width){
        if(mineArr[x][y - 1].isMine == true){
            surroundingMines++; 
        }
    }

    //To find top left diagonal do x + 1 and then y - 1
    if(x + 1 < height){
        if(mineArr[x + 1][y-1].isMine == true){
            surroundingMines++; 
        }
    }

    //To find the top right diagonal do x + 1 and then y + 1
    if(x + 1 < height){
        if(mineArr[x+1][y + 1].isMine == true){
            surroundingMines++; 
        }
    }

    //To find bottom left diagonal do x - 1 and then y - 1
    if(x - 1 > height){
        if(mineArr[x-1][y-1].isMine){
            surroundingMines++; 
        }
    }

    //To find bottom right diagonal do x - 1 and then y + 1
    if(x - 1 > height){
        if(mineArr[x-1][y+1].isMine){
            surroundingMines++; 
        }
    }


    return surroundingMines; 
}


int Board::spcCnt(){

    int tmpCnt = 0; 

    for(int i = 0; i < height; i++){
        for(int j = 0; j < width; j++){
            if(mineArr[i][j].isMine == false and mineArr[i][j].isRevealed == false){
                tmpCnt++; 
            }
        }
    }

    return tmpCnt; 
}


int Board::retrieveHeight(){return height;}
int Board::retrieveWidth(){return width;}