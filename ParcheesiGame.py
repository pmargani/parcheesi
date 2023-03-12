import random

from Constants import *
from Board import Board
from Player import Player

class ParcheesiGame:

    def __init__(self, numPlayers, verbosity=None, rolls=None, strategy=None):

        self.verbosity = 0
        if verbosity is not None:
            self.verbosity = verbosity

        self.numPlayers = numPlayers
        self.rolls = rolls
        self.strategy = strategy

        self.board = Board()

        self.players = []
        for i in range(self.numPlayers):
            p = Player(i)
            # print(p.getDescription())
            self.players.append(p)

        self.gameDone = False

        self.turn = 0
        self.rollIdx = 0    

        # game stats
        self.winTurns = 0
        self.turns = 0
        self.blocks = 0
        self.kills = 0
        self.deaths = 0
        self.doubles = 0
        self.doubleDeaths = 0

    def play(self):
        "play the game!"

        winners = []

        while not self.gameDone:

            if self.verbosity > 0:
                self.board.printBoard(self.players)

            # take turns
            for p in self.players:
                if self.gameDone:
                    break

                # players that are done don't get a turn
                if p.allPiecesAtHome():
                    continue

                if self.verbosity > 0:
                    print("Turn %d for %s" % (self.turn, p))
                    for pc in p.pieces:
                        print("  %s" % pc)

                # roll!
                doubles = 0
                rolling = True
                while rolling:

                    if self.rolls is None:
                        d1, d2 = self.roll()
                    else:
                        d1, d2 = self.rolls[self.rollIdx]
                        self.rollIdx += 1

                    if self.verbosity > 0:
                        print(" Roll: ", d1, d2)

                    # check for doubles
                    if d1 != d2:
                        # no doubles, turn is over
                        rolling = False
                    else:
                        # keep track of how many
                        # doulbes we get, cause we die
                        # after 3
                        doubles += 1
                        p.doubles += 1
                        if doubles >= 3:
                            self.loseBestPiece(p)
                            p.doubleDeaths += 1
                            rolling = False
                            break

                    # move up to two pieces!
                    # first move
                    moved = self.movePiece(p, d1, self.strategy)
                    if not moved:
                        if self.verbosity > 0:
                            print("%s could not move %d" % (p, d1))
                        p.blocked += 1

                    moved = self.movePiece(p, d2, self.strategy)    
                    if not moved:
                        if self.verbosity > 0:
                            print("%s could not move %d" % (p, d2))
                        p.blocked += 1

                if p.allPiecesAtHome():
                    p.rank = len(winners) + 1
                    winners.append(p)

                # turn is done
                self.turn += 1
                p.turns += 1

                # everyone home?
                self.gameDone = self.isGameDone()
                if self.gameDone:
                    break
            


        if self.verbosity > 0:
            self.board.printBoard(self.players)
            print("Game Over")
            print("num turns: ", self.turn)
            print("winners: ")
            for p in self.players:
                print("%s" % p)
                print("  was blocked %d times" % p.blocked)
            for i, p in enumerate(winners):
                print(i+1, " : ", str(p))

        # collect status
        winner = None
        for p in self.players:
            self.turns += p.turns
            self.blocks += p.blocked  
            self.doubles += p.doubles
            self.doubleDeaths += p.doubleDeaths
            self.kills += p.getKills()
            self.deaths += p.getDeaths()

            if p.rank == 1:
                winner = p

        self.winTurns = winner.turns * self.numPlayers

        if self.verbosity > 0:
            print("Game Stats: ")
            print("Win Turns: %d" % self.winTurns)
            print("Turns: %d" % self.turns)
            print("Blocks: %d" % self.blocks)
            print("Kills: %d" % self.kills)
            print("Deaths: %d" % self.deaths)
            print("Doubles: %d" % self.doubles)
            print("Double Deaths: %d" % self.doubleDeaths)

    def allPlayersDone(self):
        "Do all the players have all their pieces at home"

        for p in self.players:
            if not p.allPiecesAtHome():
                return False
        return True

    def hasLegalMove(self, player, d1, d2):

        for pc in player.pieces:
            if self.isMoveLegal(pc, d1):
                return True
            if self.isMoveLegal(pc, d2):
                return True
        return False
                
    def nextTurn(self):
        self.turn += 1
        if self.turn >= self.numPlayers:
            self.turn = 0
        return self.turn
            
    def roll(self):
        d1 = random.randint(1,6)
        d2 = random.randint(1,6)
        return d1, d2

    def isGameDone(self):
        "Are we done?"
        # if we're using predetermined rolls, then
        # finish up when we don't have any left
        if self.rolls is not None:
            print("len rolls vs rolIdx: ", self.rolls, self.rollIdx)
            if len(self.rolls) < self.rollIdx+1:
                return True
        return self.allPlayersDone()
                                    
    def moveSimple(self, player, die):
        if die == 5 and player.hasPieceAtBase():
            # move a piece from base to start
            pc = player.movePieceToStart()
            #if pc.startPosition not in self.board:
            #    board[pc.startPosition] = []
            #board[pc.startPosition].append(pc)   
            self.board.movePieceToStart(pc)
            return
        # move any piece past start forward  
        for pc in player.pieces:
            if pc.isOnBoard():
                oldPos = pc.position
                pc.advancePosition(die)
                newPos = pc.position
                # updateBoard(pc, oldPos, newPos, board)
                board.update(pc, oldPos, newPos)
                break   


    def isMoveLegal(self, piece, stepSize):

        legal = True

        # special starting case
        if piece.atBase():
            if stepSize == START_ROLL:
                return self.board.numPiecesOnBoardPos(piece.startPosition, piece) < 2
            else:
                # only a certain roll gets you out of base
                return False

        # pos = piece.position
        for step in range(1, stepSize+1):
            stepPos = piece.getNextPosition(step)

            if stepPos is None:
                legal = False
                break

            if self.board.numPiecesOnBoardPos(stepPos, piece) >= 2:
                legal = False
                break

        return legal

    def canMovePieceOutOfBase(self, player, die):
        "Are conditions right that a player can move a piece out of base/nest"
        return die == 5 and player.hasPieceAtBase() and self.board.isStartOpen(player)

    def canGetPieceHome(self, player, die):
        "Can this player get a piece home?"
        can = False
        pc = player.pieceCanGetHome(die)
        if pc is not None:
            can = self.isMoveLegal(pc, die)    
        return can

    def getPieceHome(self, player, die):
        "Assuming it's legal, move a piece to HOME"

        pc = player.pieceCanGetHome(die)
        oldPos = pc.position
        pc.position = HOME
        # updateBoard(pc, oldPos, HOME, board)
        self.board.update(pc, oldPos, HOME)
        return pc

    def movePieceToStart(self, player):
        "move a piece from base to start"
        pc = player.movePieceToStart()
        # if pc.startPosition not in board:
        #     board[pc.startPosition] = []
        # board[pc.startPosition].append(pc) 
        self.board.movePieceToStart(pc)
        return pc

    def movePiece(self, player, die, strategy=None):
        "Interface for moving a players piece according to the die and what is legal on the board"
        if strategy is None:
            return self.moveLegal(player, die)
        
        move = True
        options = self.getMoveOptions(player, die)
        if len(options) == 0:
            # this player has no options to move
            move = False
        elif len(options) == 1:
            # only one option!  have to do it!
            self.moveLegal(player, die)

        else:
            self.moveViaStrategy(player, die, options, strategy)
        return move
            
    def moveViaStrategy(self, player, die, options, strategy):
        """
        Pick the move that aligns with our given strategy
        """

        # a strategy lists the priorities for certain options.
        # if an option is not listed, then it's a last resort
        # and all last resorts have equal low priority


        opt = self.pickOption(options, strategy)
        if opt is None:
            # we just going to make a legal move
            piece = self.moveLegal(player, die)
        else:
            # make the move according to the strategy
            moveOpt, piece = opt
            if moveOpt == START_PIECE:
                piece = self.movePieceToStart(player)
            elif moveOpt == GET_HOME:
                piece = self.getPieceHome(player, die)
            else:
                # all other moves are covered here
                oldPos = piece.position
                newPos = piece.getNextPosition(die)
                piece.position = newPos
                # updateBoard(piece, oldPos, newPos, board)
                self.board.update(piece, oldPos, newPos)

        return piece        

    def pickOption(self, options, strategy):
        """
        Simply pick the option that gets the highest score from the strategy
           * options: [(str, Piece)]
           * strategy: {str: int}
        """
        maxOpt = None
        for optStr, piece in options:
            if optStr not in strategy:
                continue
            optScore = strategy[optStr]
            if maxOpt is None: # or optScore > maxOpt[0]:
                maxOpt = (optStr, piece)
            else:
                maxStrategy, maxPiece = maxOpt
                maxScore = strategy[maxStrategy]
                if optScore > maxScore:
                    maxOpt = (optStr, piece)    
        return maxOpt
                

    def moveLegal(self, player, die):
        """
        Make a legal move, using this strategy:
           * if you can get piece to start, do that
           * if you can get piece to home, do that
           * otherwise, just advance the first piece you can
        """   
        moved = False

        # first priority is to get a piece out of base
        #if die == 5 and player.hasPieceAtBase() and startIsOpen(player, board):
        if self.canMovePieceOutOfBase(player, die):
            # # move a piece from base to start
            # pc = player.movePieceToStart()
            # if pc.startPosition not in board:
            #     board[pc.startPosition] = []
            # board[pc.startPosition].append(pc) 
            pc = self.movePieceToStart(player)
            moved = True  
            if self.verbosity > 0:
                print("Moving piece %s to start" % pc)
        elif self.canGetPieceHome(player, die):
            pc = self.getPieceHome(player, die)
            if self.verbosity > 0:
                print("Moving piece %s to HOME" % pc)

            moved = True
        else:    
            # move any piece past start forward  
            for pc in player.pieces:
                if pc.isOnBoard():
                    oldPos = pc.position
                    newPos = pc.getNextPosition(die)
                    # newPos = pc.position
                    if self.isMoveLegal(pc, die):
                        if self.verbosity > 0:
                            print("moving piece %s to %d" % (pc, newPos))
                        pc.position = newPos
                        # updateBoard(pc, oldPos, newPos, board)
                        self.board.update(pc, oldPos, newPos)
                        moved = True
                        break 
        return moved

    def getMoveOptions(self, player, die):

        options = []
        if self.canMovePieceOutOfBase(player, die):
            options.append(('START_PIECE', None))
        if self.canGetPieceHome(player, die):
            pc = player.pieceCanGetHome(die)
            options.append(('GET_HOME', pc))
        for pc in player.pieces:
            if pc.isOnBoard():
                oldPos = pc.position
                newPos = pc.getNextPosition(die)    
                if self.isMoveLegal(pc, die): 
                    # OK, we can move this piece, but what kind of move is it?
                    if newPos in SAFE_POSITIONS:
                        options.append(('GET_SAFE', pc))
                    # TBF: we need to take into account getting into the home stretch as well    
                    #elif isNewPositionSafe(): 
                    #    options.append(('GET_SAFE', pc))    
                    elif self.board.isOccupiedByOtherPlayer(newPos, player):
                        options.append(('MAKE_KILL', pc))
                    elif self.board.isOccupiedByPlayer(newPos, player):
                        options.append(('MAKE_BLOCKADE', pc))
                    else:
                        # the piece can simply move forward, other details not known
                        options.append(('MOVE_FORWARD', pc))        

        return options

                
    def loseBestPiece(self, player):

        bestPiece = player.getBestPieceOnBoard()
        # send it back!
        if bestPiece is not None:
            # removeFromBoard(bestPiece, board)
            self.board.removeFromBoard(bestPiece)
            bestPiece.position = BASE

    def printBoard(self, players):
        "Use ascii art to represent 1 base + 64 positions + 8 home path + 1 home for each piece"

        numCols = (len(players)*4) + 3
        print("*"*numCols)
        positions = range(BASE, HOME+1)
        for pos in positions:
            s = "%02d " % pos
            for p in players:
                for pc in p.pieces:
                    if pc.position == pos:
                        s += "%s" % pc.id
                    else:
                        s += " "
            print(s)
        print("*"*numCols)     

def main():
    # quick tests:
    g = ParcheesiGame(4, verbosity=1)
    g.play()

if __name__ == '__main__':
    main()               