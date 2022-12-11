/*
    Coded By: Cedric Men 
    Date: JUL 16, 2020 
*/

#include "interaction.h"
#include <fstream> 


Interaction::Interaction(){
    gameDone = false; 
    boardptr = new Board; 
    askDimension(); //Will set dimensions

}

Interaction::~Interaction(){
    if(boardptr != NULL){
        delete boardptr; 
        boardptr = NULL; 
    }
}

void Interaction::askDimension(){
    
    bool badAnswer = true;  

    int h_in = 0; 
    int w_in = 0; 


    std::cout<<"WARNING: Please be aware that the dimensions must be at least a 1 x 1"<<std::endl<<std::endl; 
    
    while(badAnswer){
        std::cout<<"Enter A Height Of Board: ";
        std::cin>>h_in; 
        if(std::cin.fail() or h_in == 0){
            std::cin.clear(); 
            std::cin.ignore(1000,'\n');
            std::cout<<"Error, Invalid int"<<std::endl; 
        }else if(std::cin.fail() == false){badAnswer = false;}
    }

    badAnswer = true; 

    while(badAnswer){
        std::cout<<"Enter a Width of Board: "; 
        std::cin>>w_in; 
        if(std::cin.fail() or w_in == 0){
            std::cin.clear(); 
            std::cin.ignore(1000,'\n');
            std::cout<<"Error, Invalid int"<<std::endl; 
        }else if(std::cin.fail() == false){badAnswer = false;}

    }

    //Begin Setting up Board
    boardptr->setDimensions(h_in, w_in); 
    boardptr->allocateArr(); 
    boardptr->assignMines(); 

    //Print Intial Board
    boardptr->printBoardInit(); 

}

void Interaction::refresh(){
    //Display Stats: 
    system("clear"); 
    std::cout<<"Mines Total Count: "<<boardptr->cntMinesRem()<<std::endl<<std::endl; 
    boardptr->refreshBoard(); 
}

void Interaction::selectCoord(){
    
    int x_coord = 0; 
    int y_coord = 0; 

    bool badAnswer2 = true; 

    while(badAnswer2){
        std::cout<<"Enter a Row: "; 
        std::cin>>x_coord; 
        if(std::cin.fail()){
            std::cin.clear(); 
            std::cin.ignore(1000, '\n');
        }else if(x_coord >= boardptr->retrieveHeight()){
            std::cout<<"OUT OF RANGE, TRY AGAIN"<<std::endl<<std::endl; 
        }else{badAnswer2 = false;}
    }

    badAnswer2 = true; 

    while(badAnswer2){
        std::cout<<"Enter a Col: "; 
        std::cin>>y_coord; 
        if(std::cin.fail()){
            std::cin.clear(); 
            std::cin.ignore(1000, '\n');
        }else if(y_coord >= boardptr->retrieveWidth()){
            std::cout<<"OUT OF RANGE, TRY AGAIN"<<std::endl<<std::endl; 
        }else(badAnswer2 = false);
    }

    //Now Go To Coordinate, and check for game over
    bool spc = false; 
    int checker = whattoDo(x_coord, y_coord); 
    int checkBoard = boardptr->gotoLocation(x_coord, y_coord);

    if(checker == -5 or checkBoard == -5){
        errOccured(); 
    }else if(checker == 1){
        boardptr->flagElem(x_coord, y_coord); 
    }else if(checker == 2 && checkBoard == 3){
        gameDone = true; 
        gameOver(false); 
        return; 
    }else if(checker == 2 && checkBoard == 0){
        boardptr->revealElem(x_coord, y_coord);
        spc = true;  
    }

    if(boardptr->spcCnt() == 0){
        system("clear");
        gameDone = true; 
        gameOver(true); 
        return; 
    } 

    
    refresh(); 
    std::cout<<"Total Mines: "<<boardptr->cntMinesRem()<<std::endl;
    if(spc == true){
        std::cout<<"Surrounding Mines: "; 
        std::cout<<boardptr->revealSurroundingCnt(x_coord, y_coord)<<std::endl;
    }
}


int Interaction::whattoDo(int x, int y){

    char ans = ' '; 
    std::cout<<std::endl; 
    std::cout<<"What would you lke to do?(F/R): "; 
    std::cin>>ans; 

    switch (ans){
        case 'F':
        case 'f':{
            std::cout<<"Flagged"<<std::endl;
            return 1; 
            break; 
        }
        case 'R': 
        case 'r': {
            std::cout<<"Will Reveal"<<std::endl; 
            return 2; 
            break; 
        }
        default:{
            std::cout<<"Invalid Choice"<<std::endl;
            whattoDo(x, y); 
        }

    };

    return -5; 
}


bool Interaction::isGameDone(){
    return gameDone; 
}

void Interaction::gameOver(bool win){
    
    if(win == false){
        std::cout<<"GAME OVER, YOU LOST, LOSER!!!"<<std::endl;  
    }else{
        std::cout<<"CONGRATS, YOU WON!!! :)"<<std::endl; 
    }
    std::cout<<"Revealed Board: "<<std::endl; 
    boardptr->revealBoard(); 
}

void Interaction::errOccured(){
   if(boardptr != NULL){
        delete boardptr; 
        boardptr = NULL; 
   }
    exit(0); 
}