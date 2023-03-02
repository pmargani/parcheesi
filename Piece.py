from Constants import *


class Piece:

    def __init__(self, id, player):

        self.id = id
        self.player = player
        self.startPosition = player.startPosition
        self.homePathStartPosition = player.homePathStartPosition


        self.position = BASE

        self.kills = 0
        self.deaths = 0

        # pygame stuff
        self.screenPosition = None

    def __str__(self):
        return "Piece %d (%d) at position %d" % (self.id, self.player.id, self.position)

    def __repr__(self):
        return "Piece %d (%d) at position %d" % (self.id, self.player.id, self.position)


    def __eq__(self, other):
        return self.id == other.id and self.player == other.player

    def relativePosition(self, pos = None, fromPos = None):
        "How far has piece moved since start?"
        if pos is None:
            pos = self.position
        if fromPos is None:
            fromPos = self.homePathStartPosition  
        dist = pos - fromPos
        print('Pos ', pos, ' startPos ', fromPos, ' dist ', dist)
        if (pos < fromPos):
            dist = BOARDLENGTH  - (fromPos - pos)
            print(' wraparoudn for dist: ', dist)

        return dist
            
    def isOnBoard(self):
        return not self.atBase() and not self.atHome()

    def atBase(self):
        return self.position == BASE        

    def atHome(self):
        return self.position >= HOME

    def isInHomePath(self):
        return self.position > BOARDLENGTH and self.position < HOME    
    
    def isOnMainBoard(self):
        return self.isOnBoard() and not self.isInHomePath()

    def distanceFromStart(self):
        "How far has this piece traveled since it started?"
        if self.atBase():
            return 0
        if self.isInHomePath() or self.atHome():  
            return self.position - STARTOFFSET
        # piece is on main board       
        if self.position >= self.startPosition:
            return self.position - self.startPosition
        else:
            # take wrap around into account
            return (BOARDLENGTH - self.startPosition) + self.position 

    def advancePosition(self, step):
        """
        Move the piece forward, but make sure we take into
        account board absolute position wraparound and home path
        """
        self.position = self.getNextPosition(step)
        return self.position

    def pastHomeStartPosition(self, position):
        return position > self.homePathStartPosition - 1


    def getNextPosition(self, step):
        
        # first, special cases of no motion possible    
        if self.position == BASE and step != 5:
            print("In Base, can't advancePostion")
            return BASE
        if self.position >= HOME:
            print("Already Home, can't advancePosition")
            return HOME

        # special case of getting out of base
        if self.position == BASE and step == 5:
            return self.startPosition
        
        # try the basic arithmatic, then check for 
        # wrap around and going up home path
        pos = self.position
        nextPos = self.position + step
        newPos = None

        # player 0 does not have to wrap around
        if self.player.id == 0:
            if nextPos > HOME:
                newPos = HOME
            else:
                newPos = nextPos
            return newPos
                    

        if pos <= self.homePathStartPosition and nextPos > self.homePathStartPosition:
            # print("move into home path")
            diff = self.homePathStartPosition - pos
            newPos = BOARDLENGTH + step - diff
        elif pos <= BOARDLENGTH and nextPos > BOARDLENGTH:
            # print("wrapping around ", nextPos)
            newPos = nextPos - BOARDLENGTH

        elif nextPos > HOME:
            # you can't overshoot past home!
            # don't return None, instead, show how it didn't move
            newPos = pos
        else:
            # print("simple advance")
            newPos = nextPos
            # once you get past home, you're home
            # if newPos > HOME:
                # newPos = HOME
        return newPos

    def canGetHome(self, step):
        if self.position == HOME:
            # already home
            return False
        nextPos = self.getNextPosition(step)
        if nextPos is None:
            return False
        else:
            return nextPos == HOME    

            