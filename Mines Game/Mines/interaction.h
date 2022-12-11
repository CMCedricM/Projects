/*
    Coded By: Cedric Men 
    Date: JUL 16, 2020 
*/

#ifndef INTERACTION_H
#define INTERACTION_H
#include <iostream> 
#include <iomanip> 
#include <cctype>
#include "board.h"


class Interaction{

    private: 
    Board *boardptr; 
    bool gameDone; 


    public: 
    //Constructors
    Interaction(); 
    ~Interaction(); 

    //Functions To Run
    void askDimension(); 
    void selectCoord(); 
    int whattoDo(int x, int y); 
    void refresh(); 
    //Display Screen when Game is Over
    void gameOver(bool win); 
    //Check For End condition
    bool isGameDone(); 
    //If there was some wierd error, leave
    void errOccured(); 
};








#endif 