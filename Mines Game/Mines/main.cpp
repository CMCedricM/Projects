/*
    Coded By: Cedric Men 
    Date: JUL 16, 2020 
*/

#include "board.h"
#include "interaction.h"
#include <iostream>
#include <fstream> 
#include <cstdlib>

int main(int argc, char **argv){

    system("clear"); 

    srand(time(NULL)); //Set seed

    Interaction *ptr = NULL;
    ptr = new Interaction; 

    //Game 
    do{
        ptr->selectCoord(); 

    }while(ptr->isGameDone() == false); 

    delete ptr; 

    ptr = NULL; 

}