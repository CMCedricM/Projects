import tkinter as tk

class COUNTER: 
    def __init__(self):
        self.CNT = 0 
        self.WINDOW = None 
        self.createAWindow()

    def createAWindow(self): 
        
        self.WINDOW = tk.Tk()
        self.WINDOW.title("Counting Program")
        self.WINDOW.geometry("400x120")
        
    def getCnt(self): 
        return str(self.CNT)
        

    def increment(self, labelRef): 
        self.CNT += 1
        self.updateLabel(labelRef)
        
        
    def decrement(self, labelRef): 
        if not self.CNT - 1 < 0:
            self.CNT -=1
        self.updateLabel(labelRef)

    def saveCnt(self, cnt):  
        self.CNT = cnt
        print(self.CNT)
        self.WINDOW.destroy()

    def startCount(self): 
        submit = tk.Entry(self.WINDOW, bd = 1)
        submitButton = tk.Button(self.WINDOW, text="Save Start Count", command=lambda:self.saveCnt(int(submit.get())))

        submit.pack()
        submitButton.pack()

        tk.mainloop()
    
    def updateLabel(self, labelRef): 
        labelRef.config(text="Current Count = " + self.getCnt())

    def CntrWindows(self): 
       self.createAWindow()
       cntLabel = tk.Label(self.WINDOW,font="Hevetica 11 bold", text="Current Count = " + self.getCnt())
       cntLabel.grid(column=0)
       tk.Button(self.WINDOW, text="Increment", command=lambda:self.increment(cntLabel)).grid(column=1,row=3)
       tk.Button(self.WINDOW, text="Decrement", command=lambda:self.decrement(cntLabel)).grid(column = 2, row = 3)
       tk.mainloop()


    

def main(): 
    print("There's Nothing Here, LUUL")
    start = COUNTER()
    start.startCount()
    start.CntrWindows()


if __name__ == "__main__":
    main()