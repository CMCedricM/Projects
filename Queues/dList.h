#include <iostream> 


struct Node{
    int data; 
    Node *next, *prev; 
    Node(int dataIn): data(dataIn), next(NULL), prev(NULL){}; 
};


class LList{
    private: 
    Node *head, *tail; 
    
    // Deallocate Linked List
    void deleteData(){
        Node *curr = head; 
        while(curr){
            Node *temp = curr; 
            curr = curr->next; 
            delete temp; 
            temp = NULL; 
        } 
        curr = NULL; 
    }

    public: 
    // Constructors
    LList():head(NULL), tail(head){}; 
    ~LList(){ deleteData(); }
    //Exterior Remover
    void deallocate(){ deleteData(); }
    // Functions
    void insertData(int data){
        Node *newNode = new Node(data); 
        if(head == NULL){ 
            head = tail = newNode; 
        }else{ 
            Node *temp = tail; // Just having fun w/ doubly linked list
            tail->next = newNode; 
            tail = newNode; 
            tail->prev = temp; 
        }

    }

    void printFor(){
        
        Node *curr = head; 
        while(curr){ 
            std::cout<<(curr->data)<< " ";
            curr = curr->next; 
        }
        std::cout<<std::endl; 

    }

    void printBack(){
        
        Node *curr = tail; 
        while(curr){
            std::cout<<curr->data<<" ";
            curr = curr->prev; 
        }
        std::cout<<std::endl; 
    }


};