from Classes import Grams as Gram


def findWord(word, uniG = None):
    
    if uniG == None: 
       print("Error, No input gram detected")
       exit(0)

    
    word = word.lower() 
    
    for i in range(len(uniG)): 
        if word == uniG[i].word: 
            return i

    return 0

def findWord2(word1, word2, biG = None): 

    if biG == None: 
        print("Error, No input gram detected")
        return -5
    
    word1 = word1.lower()
    word2 = word2.lower()

    for i in range(len(biG)): 
        if word1 == biG[i].word1 and word2 == biG[i].word2: 
            return i 
    
    return 0 



def main(): 
    
    try: 
        grams = Gram.Gram(input("Enter a file name: "))
    except Exception as Error: 
        print("There was an error: " + str(Error))
        exit(0)

    print("Total Words Read: " + str(len(grams.dataArr)))  # To Print the Total number of words read 


    # Create Grams
    print("Please Wait, Grams Are Being Created")
    grams.createUnigram()
    uniG = grams.retUnigram()
    grams.createBigrams()
    biG = grams.retBigram()
    
    print("Unigrams and Bigrams Have Been Generated, Trigram Creation Started, this may take some time")
    grams.createTrigram()
    triG = grams.retTrigram()
    triGramFlag = True # May implement asking whether user wants to create trigrams later

    




    isDoneBool = True 
    lines = "-----------------------------------------------------------------------"

    while isDoneBool: 
        print(lines)
        print("Acceptable Commands: ")
        print(lines)
        print("Unigram: Create and Search for An Element in a Unigram")
        print("Bigram: Search For A Bigram")
        print("Save: Create and Save Files Containing the Unigrams and Bigrams")
        print("Index: Print information at an Index of the Unigram or Bigram")
        print("Q/Quit: Will Exit Program")
        print(lines)
        userInput = input("Enter Your Selection: ")
        print(lines)

        userInput = userInput.lower()

        if userInput == "unigram":
            
            wordSearch = str(input("Enter A Word to Search For: ")).lower()
            print("Searching for: " + wordSearch)
            location = int(findWord(wordSearch, uniG))
            
            if location == 0: 
                print("This word was not found in the Unigrams, try again...")
            elif location > 0: 
                print("Unigram Word Found at Index: " + str(location))
        elif userInput == "bigram": 

            wordSearch = str(input("Enter First Word: ")).lower()
            wordSearch2 = str(input("Enter Second Word: ")).lower()
            location = int(findWord2(wordSearch, wordSearch2, grams.retBigram()))
            if location == 0: 
                print("The Phrase was not found")
            elif location > 0: 
                print("The Phrase was found at Index: " + str(location))
        elif userInput == "save": 
            
            print("Grams will be sorted by frequency and then saved to a file, this may take some time so pls wait....")
            #Sort Grams
            grams.sort(uniG)
            grams.sort(biG)

            #print Unigrams
            fileHolderUnig = "uniG.txt"
            grams.writeUnigrams(fileHolderUnig)
            print("Unigrams finished, continuing to Bigrams....")

            #print Bigrams
            fileHolderBig = "biG.txt"
            grams.writeBigrams(fileHolderBig)
            print("Bigrams finished")

            if triGramFlag == True: 
                print("Will now begin sorting and saving trigrams....")
                grams.sort(triG)
                fileHolderTrig = "triG.txt"
                grams.writeTrigrams(fileHolderTrig)
                print("Trigrams finished")
                
            print(lines)
            print("Data Saved and Organized by Frequency...")
            print(lines)
        elif userInput == "index": 
            
            while True: 
                
                gramSearch = str(input("Search Unigram or Bigram for the index?(Unigram/Bigram): ")).lower()

                if gramSearch == "unigram" or gramSearch == "bigram": 
                    break
                elif gramSearch == "quit" or gramSearch == "q": 
                    exit(0)
                else: 
                    print("Not a valid option, pls try again or if you meant to quit simply type \"quit\" or \"q\"")
                
            location = int(input("Enter an Index Location: "))
            print(lines)
            if gramSearch == "unigram" and location < len(uniG): 
                if location < 0: 
                    print("Index out of bounds, please try an index from location 0 until " + str(len(uniG)))
                else: 
                    print("Unigram at index " + str(location) + " : \"" + str(uniG[location].word) + "\" with frequency " + str(uniG[location].frequency))
            elif gramSearch == "bigram" and location < len(biG): 
                if location < 0: 
                    print("Index out of bounds, please try an index from location 0 until " + str(len(biG)))
                else: 
                    print("Bigram at index " + str(location) + ": \"" + str(biG[location].word1) + " " + str(biG[location].word2) + "\" with frequency " + str(biG[location].frequency))
        elif userInput == "quit" or userInput == "q": 
            print("Thank you, now quitting...")
            break
        else: 
            print("There was an error, please try again....")

        print('\n')



            

if __name__ == "__main__": 
    main()

