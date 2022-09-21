import random

from Constants import *

def allPlayersDone(players):
    "Do all the players have all their pieces at home"


    for p in players:
        if not p.allPiecesAtHome():
            return False
    return True

def roll():
    d1 = random.randint(1,7)
    d2 = random.randint(1,7)
    return d1, d2

def isGameDone(players, turn, rolls):
    if rolls is not None:
        if len(rolls) <= turn:
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
    board[newPos].append(piece)
                                
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