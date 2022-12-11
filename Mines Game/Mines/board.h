/*
    Coded By: Cedric Men 
    Date: JUL 16, 2020 
*/

#ifndef BOARD_H
#define BOARD_H
#include <iostream> 
#include <iomanip>
#include <cstdlib>

static int widthManip = 4; 

struct Mines{
    char charHolder; 
    //Bools
    bool isMine; 
    bool isFlagged; 
    bool isRevealed; 
};

class Board{

private: 
//Variables to Set the Height and Width 
int height; 
int width; 

//Mine Count
int mineCount; 
int minesRevealed;

//Space count
int spaces;  

//Array That will hold Mine locations
Mines **mineArr; 

//Deallocation Function
void deleteArr(); 

public: 
//Constructor and Deconstructor
Board(); 
~Board(); 

//Functions to create board
void setDimensions(int h_in, int w_in); 
void allocateArr(); 
void assignMines(); 

//Printing Functions
void printBoardInit(); 
void revealBoard(); 
void refreshBoard();

//Functions For User Interaction via interaction class
int  gotoLocation(int x, int y);
void revealElem(int x, int y); 
void flagElem(int x, int y); 

//Mine stats
int revealSurroundingCnt(int x, int y); 
int  cntMinesRem(); 

//Retrieves the Spaces Left
int spcCnt(); 

//Getter
int retrieveHeight(); 
int retrieveWidth(); 

};


#endif 