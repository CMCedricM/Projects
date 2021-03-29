from Classes import Grams as Gram

def main(): 
    
    createGrams = Gram.Gram(input("Enter a Data File: "))
    #createGrams.createUnigram("testU.txt")
    #createGrams.writeUnigrams("uniG.txt")
    #createGrams.writeUnigrams("uniGSorted.txt")
    #createGrams.createBigrams("testB.txt")
    #createGrams.writeBigrams("big.txt")
    #createGrams.writeBigrams("biGSorted.txt")
    #gramHolder = createGrams.retBigram()



    createGrams.createTrigram()
    triG = createGrams.retTrigram()
    createGrams.writeTrigrams("triG.txt")
    createGrams.sort(triG)
    createGrams.writeTrigrams("SortedTrig.txt")


    #gramHolder = createGrams.retTrigram()
    #createGrams.sort(gramHolder)
    #createGrams.writeTrigrams()
    
  

    #for i in range(len(gramHolder)):
     #   print(gramHolder[i].word1 + " " + gramHolder[i].word2 + " ----> " + str(gramHolder[i].frequency))
    #print(createGrams.getUnigram()) 
    #print(createGrams.getMainArr())
    #print(createGrams.getLongestWord())
if __name__ == "__main__":
    main()