import random

from Constants import *
from Board import Board
from Player import Player
from Piece import Piece

def allPlayersDone(players):
    "Do all the players have all their pieces at home"


    for p in players:
        if not p.allPiecesAtHome():
            return False
    return True

def hasLegalMove(player, d1, d2, board):

    for pc in player.pieces:
        if isMoveLegal(pc, d1, board):
            return True
        if isMoveLegal(pc, d2, board):
            return True
    return False
            
def nextTurn(turn, numPlayers):
    turn += 1
    if turn >= numPlayers:
        turn = 0
    return turn
        
def roll():
    d1 = random.randint(1,6)
    d2 = random.randint(1,6)
    return d1, d2

def isGameDone(players, rollIdx, rolls):
    if rolls is not None:
        if len(rolls) <= rollIdx:
            return True
    return allPlayersDone(players)
                                
def moveSimple(player, die, board):
    if die == 5 and player.hasPieceAtBase():
        # move a piece from base to start
        pc = player.movePieceToStart()
        if pc.startPosition not in board:
            board[pc.startPosition] = []
        board[pc.startPosition].append(pc)   
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


def isMoveLegal(piece, stepSize, board):

    legal = True

    # special starting case
    if piece.atBase():
        if stepSize == START_ROLL:
            return board.numPiecesOnBoardPos(piece.startPosition, piece) < 2
        else:
            # only a certain roll gets you out of base
            return False

    # pos = piece.position
    for step in range(1, stepSize+1):
        stepPos = piece.getNextPosition(step)

        if stepPos is None:
            legal = False
            break

        if board.numPiecesOnBoardPos(stepPos, piece) >= 2:
            legal = False
            break

    return legal

def canMovePieceOutOfBase(player, die, board):
    "Are conditions right that a player can move a piece out of base/nest"
    return die == 5 and player.hasPieceAtBase() and board.isStartOpen(player)

def canGetPieceHome(player, die, board):
    "Can this player get a piece home?"
    can = False
    pc = player.pieceCanGetHome(die)
    if pc is not None:
        can = isMoveLegal(pc, die, board)    
    return can

def getPieceHome(player, die, board):
    "Assuming it's legal, move a piece to HOME"

    pc = player.pieceCanGetHome(die)
    oldPos = pc.position
    pc.position = HOME
    # updateBoard(pc, oldPos, HOME, board)
    board.update(pc, oldPos, HOME)
    return pc

def movePieceToStart(player, board):
    "move a piece from base to start"
    pc = player.movePieceToStart()
    # if pc.startPosition not in board:
    #     board[pc.startPosition] = []
    # board[pc.startPosition].append(pc) 
    board.movePieceToStart(pc)
    return pc

def movePiece(player, die, board, strategy=None):
    "Interface for moving a players piece according to the die and what is legal on the board"
    if strategy is None:
        return moveLegal(player, die, board)
    
    move = True
    options = getMoveOptions(player, die, board)
    if len(options) == 0:
        # this player has no options to move
        move = False
    elif len(options) == 1:
        # only one option!  have to do it!
        moveLegal(player, die, board)

    else:
        moveViaStrategy(player, die, board, options, strategy)
    return move
        
def moveViaStrategy(player, die, board, options, strategy):
    """
    Pick the move that aligns with our given strategy
    """

    # a strategy lists the priorities for certain options.
    # if an option is not listed, then it's a last resort
    # and all last resorts have equal low priority


    opt = pickOption(options, strategy)
    if opt is None:
        # we just going to make a legal move
        piece = moveLegal(player, die, board)
    else:
        # make the move according to the strategy
        moveOpt, piece = opt
        if moveOpt == START_PIECE:
            piece = movePieceToStart(player, board)
        elif moveOpt == GET_HOME:
            piece = getPieceHome(player, die, board)
        else:
            # all other moves are covered here
            oldPos = piece.position
            newPos = piece.getNextPosition(die)
            piece.position = newPos
            # updateBoard(piece, oldPos, newPos, board)
            board.update(piece, oldPos, newPos)

    return piece        

def pickOption(options, strategy):
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
            

def moveLegal(player, die, board, verbose=False):
    """
    Make a legal move, using this strategy:
       * if you can get piece to start, do that
       * if you can get piece to home, do that
       * otherwise, just advance the first piece you can
    """   
    moved = False

    # first priority is to get a piece out of base
    #if die == 5 and player.hasPieceAtBase() and startIsOpen(player, board):
    if canMovePieceOutOfBase(player, die, board):
        # # move a piece from base to start
        # pc = player.movePieceToStart()
        # if pc.startPosition not in board:
        #     board[pc.startPosition] = []
        # board[pc.startPosition].append(pc) 
        pc = movePieceToStart(player, board)
        moved = True  
        if verbose:
            print("Moving piece %s to start" % pc)
    elif canGetPieceHome(player, die, board):
        pc = getPieceHome(player, die, board)
        if verbose:
            print("Moving piece %s to HOME" % pc)

        moved = True
    else:    
        # move any piece past start forward  
        for pc in player.pieces:
            if pc.isOnBoard():
                oldPos = pc.position
                newPos = pc.getNextPosition(die)
                # newPos = pc.position
                if isMoveLegal(pc, die, board):
                    if verbose:
                        print("moving piece %s to %d" % (pc, newPos))
                    pc.position = newPos
                    # updateBoard(pc, oldPos, newPos, board)
                    board.update(pc, oldPos, newPos)
                    moved = True
                    break 
    return moved

def getMoveOptions(player, die, board):

    options = []
    if canMovePieceOutOfBase(player, die, board):
        options.append(('START_PIECE', None))
    if canGetPieceHome(player, die, board):
        pc = player.pieceCanGetHome(die)
        options.append(('GET_HOME', pc))
    for pc in player.pieces:
        if pc.isOnBoard():
            oldPos = pc.position
            newPos = pc.getNextPosition(die)    
            if isMoveLegal(pc, die, board): 
                # OK, we can move this piece, but what kind of move is it?
                if newPos in SAFE_POSITIONS:
                    options.append(('GET_SAFE', pc))
                # TBF: we need to take into account getting into the home stretch as well    
                #elif isNewPositionSafe(): 
                #    options.append(('GET_SAFE', pc))    
                elif board.isOccupiedByOtherPlayer(newPos, player):
                    options.append(('MAKE_KILL', pc))
                elif board.isOccupiedByPlayer(newPos, player):
                    options.append(('MAKE_BLOCKADE', pc))
                else:
                    # the piece can simply move forward, other details not known
                    options.append(('MOVE_FORWARD', pc))        

    return options

            
def loseBestPiece(player, board):

    bestPiece = player.getBestPieceOnBoard()
    # send it back!
    if bestPiece is not None:
        # removeFromBoard(bestPiece, board)
        board.removeFromBoard(bestPiece)
        bestPiece.position = BASE

def printBoard(players):
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

def play(numPlayers, strategy=None, rolls=None, verbose=False):
    
    board = Board()

    # create players
    players = []
    winners = []
    for i in range(numPlayers):
        p = Player(i)
        # start al pieces off board
        # for pc in p.pieces:
            # pc.position = p.startPosition 
        if verbose:    
            print(p.getDescription())
        players.append(p)

    gameDone = False

    turn = 0
    rollIdx = 0

    while not gameDone:
        if verbose:
            board.printBoard(players)

        # take turns
        for p in players:
            if gameDone:
                break

            # players that are done don't get a turn
            if p.allPiecesAtHome():
                continue

            if verbose:
                print("Turn %d for %s" % (turn, p))
                for pc in p.pieces:
                    print("  %s" % pc)

            # roll!
            doubles = 0
            rolling = True
            while rolling:

                if rolls is None:
                    d1, d2 = roll()
                else:
                    d1, d2 = rolls[rollIdx]
                    rollIdx += 1

                if verbose:
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
                        if verbose:
                            print("Third doubles!", d1, d2)
                        loseBestPiece(p, board)
                        p.doubleDeaths += 1
                        rolling = False
                        break

                # move up to two pieces!
                # first move
                moved = movePiece(p, d1, board, strategy)
                if not moved:
                    if verbose:
                        print("%s could not move %d" % (p, d1))
                    p.blocked += 1

                moved = movePiece(p, d2, board, strategy)    
                if not moved:
                    if verbose:
                        print("%s could not move %d" % (p, d2))
                    p.blocked += 1


                    

            if p.allPiecesAtHome():
                p.rank = len(winners) + 1
                winners.append(p)

            # turn is done
            turn += 1
            p.turns += 1

            # everyone home?
            gameDone = isGameDone(players, rollIdx, rolls)
            if gameDone:
                break
        
        

    if verbose:
        board.printBoard(players)
        print("Game Over")
        print("num turns: ", turn)
        print("winners: ")
        for p in players:
            print("%s" % p)
            print("  was blocked %d times" % p.blocked)
        for i, p in enumerate(winners):
            print(i+1, " : ", str(p))

    return players      