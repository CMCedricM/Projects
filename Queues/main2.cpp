#include <iostream>
#include <assert.h> 
#include "dList.h"

//First off, im making a queue of queues
class CircularQueue{
    
    private: 
    int front, back, size, maxSize; 
    LList **baseQueue; 

    public: 
    CircularQueue(int sizeIn = 1): front(0), back(0), size(0), maxSize(sizeIn){ 
        baseQueue = new LList*[maxSize];
        for(int i = 0; i < maxSize; i++){ baseQueue[i] = NULL; } 
    }; 

    ~CircularQueue(){        
        if(baseQueue != NULL){
            delete [] baseQueue;
            baseQueue = NULL; 
        }
    }; 

    // Functions 
    void resize(){ 
        
        maxSize = maxSize * 2; 
        // Allocate a new list but 2x the size
        LList **newList = new LList*[maxSize]; 


        // Now copy data from old list to new list 
        for(int i = 0; i < size; i++){ 
            newList[i] = baseQueue[i]; 
        }

        // Now set the front and back accordingly and adjust size
        front = 0; 
        back = size; // Size is the actual count of the amount of data in the queue 

        delete [] baseQueue; 
        baseQueue = newList; 
    }

    void enqueue(LList *linkedList){ 
        if(size == maxSize){ 
            resize(); 
        }

        //back = (back) % maxSize;
        baseQueue[back++] = linkedList; // Post increment -> use the value first then increment
        size += 1; 
    }

    void dequeue(){ 
        int removalIndex = front; 
        
        if(baseQueue[removalIndex]){
            std::cout<<"\nDequeueing Index "<<removalIndex<<": ";
            baseQueue[removalIndex]->printBack(); 
            delete baseQueue[removalIndex];  
            baseQueue[removalIndex] = NULL; 
            front += 1; 
        }else{ 
            std::cout<<"ERROR: Cannot dequeue, queue is empty"<<std::endl;
        }
    }

    //Just insert data into told section 
    void enqueue(int index, int data){ 
        if(index < maxSize){
            if(baseQueue[index] == NULL){ 
                std::cout<<"Error, This Location is NULL"<<std::endl; 
            }else{
                baseQueue[index]->insertData(data); 
            }
        }else{ 
            printf("Error invalid index....\n");
        }
    }

    void enqeueNext(int data){
        baseQueue[back-1]->insertData(data); 
    }


    void print(){ 
    
        for(int i = 0; i < maxSize - 1; i++){
            std::cout<<"Index "<<i<<": "; 
            if(baseQueue[i]){
                baseQueue[i]->printBack();
            }else{
                std::cout<<"EMPTY LIST"<<std::endl; 
            }
            
        }
    }

}; 



int main(int argc, char **argv){ 

    // The queue itself
    CircularQueue *newQueue = new CircularQueue(2);

    // The Lists to be inserted into the queue
    LList *testList = new LList; 
    LList *secondTestList = new LList; 
    LList *anotherList = new LList; 
 

    // Create First Queue in Queue array 
    newQueue->enqueue(testList); 
    for(int i = 0; i < 30; i++){
        newQueue->enqeueNext(i);
    }

    newQueue->print(); 

    //Create SEcond Queue 
    newQueue->enqueue(secondTestList); 
    for(int i = 0; i < 20; i++){
        newQueue->enqeueNext(i);
    }
    newQueue->print();

    // Create Second Qeueu in Queue array
    newQueue->enqueue(anotherList); 
    //newQueue->enqeueNext(30); 
    //newQueue->enqueue(1,2);
    for(int i = 0; i < 10; i++){
        newQueue->enqeueNext(i);
    }
    std::cout<<std::endl<<std::endl; 
    newQueue->print();
    printf("Here\n");

    //Testing Deque 
    newQueue->dequeue();
    newQueue->enqueue(1,27);
    

    //Print List One More Time
    std::cout<<std::endl; 
    newQueue->print();

    //assert(testList==anotherList); 

    // Clean Up (remove allocations)
    //delete testList; 
    delete secondTestList;
    delete anotherList; 
    delete newQueue; 

    newQueue = NULL; 
    testList = anotherList = NULL;

     
}
