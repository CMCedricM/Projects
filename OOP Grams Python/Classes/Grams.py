from Classes import GramStruc as GramStruct
import sys 
import math

# Class DataSet: This class takes in a data file and saves all the words to 
# a 1-d array, cleans the data (programmer must fill out this flag of whether to filter words with numbers), 
# and then the 1-d array can be accessed via a getter function (all data will be lowercased, and if flags are used will 
# respond accordingly)
class DataSet:

    def __init__(self, dataSetFile, aLogFile = None, nonAlphaFlag = None):

        self.mainArr = []
        self.readFile(dataSetFile, aLogFile, nonAlphaFlag)

    
    # readFile: Will read the given file, save it to the array, and then clean it
    def readFile(self, dataSetFile, aLogFile = None, nonAlphaFlag = None): 

        try: 
            dataSetFile = open(dataSetFile, 'r')
        except Exception as Err: 
            print("There was a Fatal Error: " + str(Err))
            exit(0)
        
        # Read through the file and save to the main array
        for lines in dataSetFile: 
            for aword in lines.split(): 
                self.mainArr.append(aword)
        
        dataSetFile.close()
        # End read through the file and save 

        self.cleanData(aLogFile, nonAlphaFlag)
        
    
    #cleanData: Helper function for the readFile, this will clean the data accodring 
    # according to given parameters. 
    def cleanData(self, aLogFile = None, nonAlphaFlag = None): 

        if aLogFile != None: 
            try: 
                aLogFile = open(aLogFile, 'w')
            except Exception as Err: 
                print("There was a Fatal Error: " + str(Err))
                exit(0)
        
       
        wordRet = ""
        for aword in range(len(self.mainArr)): 
            
            ConsWord = self.mainArr[aword] # Cleaned word will be compared to this to see if logging needed
            charArr = list(self.mainArr[aword])

            if nonAlphaFlag == True: 
                for i in range(len(charArr)): 
                    if charArr[i].isnumeric(): 
                        wordRet = "NONALPHA"
            
            if wordRet != "NONALPHA": 
                # Now remove any Punctuation 
                for j in range(len(charArr)): 
                    if charArr[j].isalnum(): 
                        wordRet += charArr[j]
            
            if aLogFile != None and wordRet != ConsWord: 
                if wordRet == "NONALPHA": 
                    aLogFile.write(str(ConsWord) + "--->"+ str(wordRet) + '\n')
                else: 
                    aLogFile.write(str(ConsWord) + "--->"+ str(wordRet.lower()) + '\n')
            
            if wordRet == "NONALPHA": 
                self.mainArr[aword] = wordRet
            else: 
                self.mainArr[aword] = wordRet.lower()
            
            wordRet = ""

    # getMainArr: Is a getter function that returns the 1-d array of words/data
    def getMainArr(self): 
        return self.mainArr
    
    # getLongestWord: Is a getter function that will return the longest word
    def getLongestWord(self): 
        
        longest = self.mainArr[0]

        for i in range(len(self.mainArr)): 
            if len(longest) < len(self.mainArr[i]):
                longest = self.mainArr[i]
        
        return longest



class Gram: 

    def __init__(self, dataFile, aLogFile = None, nonAlphaFlag = None): 
        
        self.data = DataSet(dataFile, aLogFile, nonAlphaFlag) 
        self.dataArr = self.data.getMainArr()
       
        
        # Create var for Grams
        self.UnigArr = []
        self.BigArr = []
        self.TrigArr = []

        # Set Recursion Limit 
        limit = int(math.log2(len(self.dataArr))) * 10000
        sys.setrecursionlimit(limit)
        

    #############################################################################
    # Begin Unigram 
    # Will see how many times the word was found in the book 
    def __cntTimesFound(self, wordToLook): 

        cnt = 0

        for i in range(len(self.dataArr)): 
            if wordToLook == self.dataArr[i]: 
                cnt += 1
        
        return cnt 


    # Will attempt to see if the given word exists in the UniGram
    def __doesExist(self, wordToLook,uniArr): 

        for i in range(len(uniArr)): 
            if wordToLook == uniArr[i].word: 
                return True
        
        return False 

    # Programmer needs to call this in order to create the unigrams
    def createUnigram(self, fileOut = None): 

        for i in range(len(self.dataArr)): 
            if self.__doesExist(self.dataArr[i],self.UnigArr) == False:
                fndCnt = int(self.__cntTimesFound(self.dataArr[i]))
                self.UnigArr.append(GramStruct.Unigram(self.dataArr[i], fndCnt))
        
        if fileOut != None: 
            self.writeUnigrams(fileOut)
        
            


                
    # Programmer can choose this option to write to file 
    def writeUnigrams(self, fileOut = None): 

        if fileOut == None: 
            for i in range(len(self.UnigArr)): 
                print(str(self.UnigArr[i].word) + ' -----> ', end = "")
                print(str(self.UnigArr[i].frequency))
            return 
                

        try: 
            fileOut = open(fileOut, 'w')
        except Exception as Error: 
            print("There was an error: " + str(Error))
            exit(0)
        
        for i in range(len(self.UnigArr)): 
            fileOut.write(str(self.UnigArr[i].word) + ' -----> ')
            fileOut.write(str(self.UnigArr[i].frequency) + '\n')
        
        fileOut.close()

        

    # Programmer can call this to obtain the unigram array
    def retUnigram(self): 
        return self.UnigArr
    
    # End Unigrams
    #############################################################################

    # Begin Bigrams
    
    def __doesExistBi(self, word1, word2): 

        for i in range(len(self.BigArr)):
            if word1 == self.BigArr[i].word1 and word2 == self.BigArr[i].word2: 
                return True

        return False

    
    def __cntTimeFound2(self, word1, word2): 

        cnt = 0 

        for i in range(len(self.dataArr) - 1): 
            if word1 == self.dataArr[i] and word2 == self.dataArr[i + 1]:
                cnt += 1 
        
        return int(cnt) 
        

    def createBigrams(self, fileOut = None): 

        for i in range(len(self.dataArr) - 1): 
            if self.__doesExistBi(self.dataArr[i], self.dataArr[i + 1]) == False: 
                foundCnt = self.__cntTimeFound2(self.dataArr[i], self.dataArr[i + 1])
                self.BigArr.append(GramStruct.Bigram(self.dataArr[i], self.dataArr[i + 1], foundCnt))

            if fileOut != None: 
                self.writeBigrams(fileOut)

                
    

    def writeBigrams(self, fileOut = None): 
        
        if fileOut == None: 
            for i in range(len(self.BigArr)): 
                print(str(self.BigArr[i].word1) + " " + str(self.BigArr[i].word2) + ' -----> ', end = "")
                print(str(self.BigArr[i].frequency))
            return 


        try: 
            fileOut = open(fileOut, 'w')
        except Exception as Error: 
            print("There was a fatal Error: " + str(Error))
            exit(0)
        
        for i in range(len(self.BigArr)): 
            fileOut.write(str(self.BigArr[i].word1) + " " + str(self.BigArr[i].word2) + ' -----> ')
            fileOut.write(str(self.BigArr[i].frequency) + '\n')
        
        fileOut.close()


    def retBigram(self): 
        return self.BigArr

    # End Bigrams
    #############################################################################

    # Begin Trigrams
    def __doesExistTri(self, word1, word2, word3):
        cnt = 0 

        for i in range(len(self.dataArr)): 
            if i+2 > len(self.dataArr) - 1: 
                break
            elif self.dataArr[i] == word1 and self.dataArr[i+1] == word2 and self.dataArr[i+2] == word3: 
                cnt = cnt + 1
        return cnt

    def __chkTriArr(self, word1, word2, word3): 
        
        for i in range(len(self.TrigArr)): 
            if self.TrigArr[i].word1 == word1 and self.TrigArr[i].word2 == word2 and self.TrigArr[i].word3 == word3:
                return True
        
        return False
    
    # This function is to be called when the programmer decides to create the trigrams
    def createTrigram(self, fileOut = None): 
        
        tracker = 0 

        while tracker + 2 < len(self.dataArr): 

            if self.__chkTriArr(self.dataArr[tracker], self.dataArr[tracker + 1], self.dataArr[tracker+2]) == False: 
                frq = self.__doesExistTri(self.dataArr[tracker], self.dataArr[tracker + 1], self.dataArr[tracker + 2])
                self.TrigArr.append(GramStruct.Trigram(self.dataArr[tracker], self.dataArr[tracker+1], self.dataArr[tracker + 2], frq))

            tracker = tracker + 2
        if fileOut != None: 
            self.writeTrigrams(fileOut)
    

    def writeTrigrams(self, fileOut = None): 
        
        if fileOut == None: 
            for i in range(len(self.TrigArr)): 
                print(self.TrigArr[i].word1 + " " + self.TrigArr[i].word2 + " " + self.TrigArr[i].word3 + " -----> " + str(self.TrigArr[i].frequency))
            return 
        
        try: 
            fileOut = open(fileOut, 'w')
        except Exception as Err: 
            print("There was a fatal error: " + str(Err))
            exit(0)
        
        for i in range(len(self.TrigArr)): 
            fileOut.write(str(self.TrigArr[i].word1) + " " + str(self.TrigArr[i].word2) + " " + self.TrigArr[i].word3 + " -----> " + str(self.TrigArr[i].frequency) + '\n')

        fileOut.close() 


    # Programmer can call this function to obtain the trigram array
    def retTrigram(self): 
        return self.TrigArr

    

    def __swap(self, gram, swap1, swap2): 
   
        tempHold = gram[swap1]
        gram[swap1] = gram[swap2]
        gram[swap2] = tempHold
        
        return gram 


    def __paritionData(self, gram, low, high): 
        lagBehind = low - 1
        pivotPt = high

        i = low 
        while(i <= high - 1): 
            if gram[i].frequency > gram[pivotPt].frequency: 
                lagBehind += 1
                self.__swap(gram, lagBehind, i)
            i += 1 
        
        # Final Swap
        self.__swap(gram, lagBehind + 1, pivotPt)
        return lagBehind + 1


    # def quicksort(Unigram uni, int low, int high)
    #   pivotAround = partition(uni[], low, high)
    #   quicksortLeft(uni[], low, pivotAround - 1)
    #   quicksortRight(uni[], pivotAround + 1, high)
    def __quickSort(self, gram, low, high): 
        
        if low < high: 
            partitionAround = self.__paritionData(gram, low, high)
            self.__quickSort(gram, low, partitionAround - 1)
            self.__quickSort(gram, partitionAround + 1, high)
        return 

    def sort(self, gramIn = None):
        
        if gramIn == None: 
            return "error, no nGram provided"
        self.__quickSort(gramIn, 0, len(gramIn) - 1) 




       