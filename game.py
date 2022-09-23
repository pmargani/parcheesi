import random

from Constants import *

def allPlayersDone(players):
    "Do all the players have all their pieces at home"


    for p in players:
        if not p.allPiecesAtHome():
            return False
    return True

def roll():
    d1 = random.randint(1,6)
    d2 = random.randint(1,6)
    return d1, d2

def isGameDone(players, rollIdx, rolls):
    if rolls is not None:
        if len(rolls) <= rollIdx:
            return True
    return allPlayersDone(players)

def updateBoard(piece, oldPos, newPos, board):

    if oldPos in board:
        # find piece and remove it
        for i, pc in enumerate(board[oldPos]):
            if pc == piece:
                board[oldPos].pop(i)
    if newPos not in board:
        board[newPos] = []
    elif len(board[newPos]) > 0 and newPos < BOARDLENGTH and newPos not in SAFE_POSITIONS:
        # there's other pieces here?  Any from other team?
        # TBF: arbitrarly pick first one
        otherPiece = board[newPos][0]
        if otherPiece.player.id != piece.player.id:
            # back to base!
            print("Kill by %s on %s" % (piece, otherPiece))
            otherPiece.deaths += 1
            otherPiece.position = BASE
            board[newPos].pop(0)
            piece.kills += 1


    board[newPos].append(piece)

    # remove other piece first
                                
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
            updateBoard(pc, oldPos, newPos, board)
            break   

def startIsOpen(player, board):

    pos = player.startPosition

    if pos not in board:
        # it's empty!
        return True
    elif len(board[pos]) < 2:
        # just one piece there!
        return True
    else:
        # it's full!
        return False

def removeFromBoard(piece, board):

    pcs = board[piece.position]
    for i, pc in enumerate(pcs):
        if pc == piece:
            pcs.pop(i)
            break

def numPiecesOnBoardPos(pos, piece, board):
    if pos not in board:
        return 0
    if pos <= BOARDLENGTH:    
        return len(board[pos])
    elif pos >= HOME:
        # act like nobodies there, since there aren't restrictions
        return 0    
    else:
        # treat the home path as four separate paths
        return len([ pc for pc in board[pos] if pc.player.id == piece.player.id])    
        
def isMoveLegal(piece, stepSize, board):

    legal = True
    # pos = piece.position
    for step in range(1, stepSize+1):
        stepPos = piece.getNextPosition(step)

        if numPiecesOnBoardPos(stepPos, piece, board) >= 2:
            legal = False
            break

    return legal

def moveLegal(player, die, board):
    moved = False
    # first priority is to get a piece out of base
    if die == 5 and player.hasPieceAtBase() and startIsOpen(player, board):
        # move a piece from base to start
        pc = player.movePieceToStart()
        if pc.startPosition not in board:
            board[pc.startPosition] = []
        board[pc.startPosition].append(pc) 
        moved = True  
    else:
        # move any piece past start forward  
        for pc in player.pieces:
            if pc.isOnBoard():
                oldPos = pc.position
                newPos = pc.getNextPosition(die)
                # newPos = pc.position
                if isMoveLegal(pc, die, board):
                    pc.position = newPos
                    updateBoard(pc, oldPos, newPos, board)
                    moved = True
                    break 
    return moved

def loseBestPiece(player, board):

    bestPiece = player.getBestPieceOnBoard()
    # send it back!
    removeFromBoard(bestPiece, board)
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