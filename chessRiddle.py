# Code for implementing a scheme to solve the chess prison riddle.
# Written with readability, NOT SPEED, in mind
# Have not implemented much error checking, this code breaks easily
# if you abuse the inputs (ie, N != 2**m)
# this algo can likely be generalized to boards of arbitrary size
# but I am lazy so for now I assume the number of squares is
# a power of 2.






import numpy as np

class board:
    """board object"""
    N = 64                              #size of board (must be power of two)
    boardState = np.full(N,True)        #default is a board of all heads

        # Represents the chess board as a 1-dimensional numpy array of 
        # dtype = bool . The mapping between the 1-d array and an actual
        # chessboard is arbitrary.
        # For consistency in the comments, assume true -> heads,
        # false -> tails (also an arbitrary mapping)

    keyIndex = np.int(0)                     #index of super secret key

    keyIndexGuess = np.int(0)       # Tracks the "guess" of the keyIndex
    nbitsIndex = np.log2(N)         # number of bits in keyIndex
                                    # (and hence keyIndexGuess)


    def __init__(self,_N):
        self.N = _N
        # initialize a random board:
        self.boardState = np.random.choice(a=[True,False], size = self.N)
        self.keyIndex = np.random.randint(self.N)
        self.nbitsIndex = np.log2(self.N).astype(int)


    def flipCoin(self,n):
        # flips the coin at index n
        self.boardState[n] = np.logical_not(self.boardState[n])

    def interpretBoardState(self,verbose = True):
        # examines the current board state and makes a guess at keyIndex.
        # The guess can be represented as a binary number of size
        # log2(N). This algorithm uses a numpy boolean array to represent
        # each bit of the guess, and then interprets the array to an int
        # at the end.
        _guess = np.full(self.nbitsIndex,False) #initialize guess to '0'

        indiciesUT = np.arange(self.N/2).astype(int)    # indicies Under Test
                                            # indicies of boardState being
                                            #considered for the current bit
                                            # of _guess (first bit will
                                            # consider the first half)

        for n in (np.arange(self.nbitsIndex)[::-1]).astype(int):
            # is the number of heads within the indicies under test
            # even? if so, set that bit of _guess to 1.
            _guess[n] = np.sum(self.boardState[indiciesUT])%2 == 0
            
            # Modify the indicies under test. This is the special sauce
            # of the solution. Must choose some pattern such that set of
            # indiciesUT shares half of its elements with EACH other set of
            # indiciesUT (this is not strictly true if N is not a power
            # of two, but again I am lazy and have not implemented that.)
            # There are multiple ways to do this. I have chosen regular
            # halfing. That is, first bit is from front half of full board state,
            # second bit is from front half of each half of board state, etc.

            if(n>0):  #don't modify on last iteration
                indiciesToModify = np.where(indiciesUT % 2**n >= 2**(n-1))[0]
                indiciesUT[indiciesToModify] += 2**(n-1)

        self.keyIndexGuess = np.sum([_guess[n]*(2**n) for n in range(self.nbitsIndex)]).astype(int)
        
        if(verbose):
            print("Board state indiciates the key is at index " + str(self.keyIndexGuess))
            print("Actual key is at " + str(self.keyIndex))


    def pickIndexToFlip(self, verbose = True):
        # Identifies the index of the coin that should be flipped so that
        # self.interpretBoardState correctly guesses keyIndex
        indexToFlip = 0

        # interpret keyIndex as a boolean array:
        keyIndexArray = np.asarray([self.keyIndex%(2**(n+1))>=2**(n) for n in np.arange(self.nbitsIndex)]).astype(bool)


        # Consider indicies using the same scheme as 
        # self.interpretBoardState. 
        # At each step, if the parity of the indicies under test
        # is already correct, then we need to modify a bit from the
        # set of indicies that is NOT being considered. This is
        # achieved by adding powers of two in reverse order
        # to the indexToFlip.

        indiciesUT = np.arange(self.N/2).astype(int)
        for n in (np.arange(self.nbitsIndex)[::-1]).astype(int):
            if ((np.sum(self.boardState[indiciesUT]) % 2 == 0) == keyIndexArray[n]):
                indexToFlip += 2**n

            if(n>0):  #don't modify on last iteration
                indiciesToModify = np.where(indiciesUT % 2**n >= 2**(n-1))[0]
                indiciesUT[indiciesToModify] += 2**(n-1)            

        if (verbose):
            print("The index to be flipped is: " + str(indexToFlip))

        self.flipCoin(indexToFlip)
