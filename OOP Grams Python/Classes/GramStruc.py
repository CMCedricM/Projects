class Unigram:
    
    def __init__(self, word1, frequency = 0):
        self.word = word1 
        self.frequency = frequency


class Bigram: 
    
    def __init__(self, word1, word2, frequency = 0): 
        self.word1 = word1
        self.word2 = word2 
        self.frequency = frequency


class Trigram: 

    def __init__(self, word1, word2, word3, frequency = 0): 
        self.word1 = word1
        self.word2 = word2
        self.word3 = word3
        self.frequency = frequency
