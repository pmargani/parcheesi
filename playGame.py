import time
import sys
import random

import pygame

from Constants import *
from game import *
from Player import Player

WIDTH = 600
HEIGHT = 800

NUMPLAYERS = 4

PIECE_RADIUS = 10

COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_GREEN = (0, 255, 0)

SCREEN_COLORS = {
    RED : COLOR_RED,
    BLUE : COLOR_BLUE,
    YELLOW : COLOR_YELLOW,
    GREEN : COLOR_GREEN,
}

BASE_SIDE_OFFSET = 135

bo = 260
BASE_OFFSETS = [
    (0, 0),
    (0, bo),
    (bo, bo),
    (bo, 0),

]

po = 25
BASE_PIECE_OFFSETS = [
    (0, 0),
    (po, 0),
    (po, po),
    (0, po)
]

BOARD_START_X = 80
BOARD_START_Y = 85
BOARD_INNER_OFFSET = 262

# draw lines to figure out board layour
posWidth = 45
posHeight = 16

board = {}
turn = 0
playerTurn = 0
players = []
winners = []
for i in range(NUMPLAYERS):
    p = Player(i)
    # start al pieces off board
    # for pc in p.pieces:
        # pc.position = p.startPosition 
    print(p.getDescription())
    players.append(p)


def getBoardPositions():
    


    # y = WIDTH/2
    # x = WIDTH
    # start = (0, y)
    # end = (x, y)
    # screen.draw.line(start, end, color='black')
    # start = (0, y-posWidth)
    # end = (x, y-posWidth)
    # screen.draw.line(start, end, color='black')

    # x = WIDTH/2 + 5
    # y = WIDTH
    # start = (x, 0)
    # end = (x, y)
    # screen.draw.line(start, end, color='black')
    # posWidth = 50
    # start = (x-posWidth, 0)
    # end = (x-posWidth, y)
    # screen.draw.line(start, end, color='black')

    boardScreenPositions = [
        (WIDTH/2 + 5 - (posWidth/2), BOARD_START_Y),
        # (WIDTH/2 + 5 - posWidth - (posWidth/2), BOARD_START_Y),
        # (WIDTH/2 + 5 - posWidth - (posWidth/2), BOARD_START_Y + posHeight),
        # (WIDTH/2 + 5 - posWidth - (posWidth/2), BOARD_START_Y + 2*posHeight),
    ]
    
    laneLen =8 

    lane1 = [(WIDTH/2 + 5 - posWidth - (posWidth/2), BOARD_START_Y + i*posHeight) for i in range(0,laneLen)]
    
    boardScreenPositions.extend(lane1)

    revLanes = list(range(laneLen))
    revLanes.reverse()
    
    lane2 = [(BOARD_START_X + posHeight/2 + i*(posHeight+1), (WIDTH/2) - posWidth - (posWidth/2)) for i in revLanes]

    boardScreenPositions.extend(lane2)

    boardScreenPositions.append((BOARD_START_X + posHeight/2,WIDTH/2 - posWidth/2))
    
    lane3 = [(BOARD_START_X + posHeight/2 + posHeight*i ,WIDTH/2 - posWidth/2 + posWidth) for i in range(0, laneLen)]

    boardScreenPositions.extend(lane3)

    # like lane 1, but further down y
    lane4 = [(WIDTH/2 + 5 - posWidth - (posWidth/2), BOARD_START_Y + BOARD_INNER_OFFSET + i*posHeight) for i in range(0,laneLen)]

    boardScreenPositions.extend(lane4)

    boardScreenPositions.append((WIDTH/2 + 5 - (posWidth/2), BOARD_START_Y + BOARD_INNER_OFFSET + 7*posHeight))

    lane5 = [(WIDTH/2 + 5 + (posWidth/2), BOARD_START_Y + BOARD_INNER_OFFSET + i*posHeight) for i in revLanes]

    boardScreenPositions.extend(lane5)

    # lane 6 is like lane 3
    lane6 = [(BOARD_START_X + BOARD_INNER_OFFSET + posHeight/2 + posHeight*i ,WIDTH/2 - posWidth/2 + posWidth) for i in range(0, laneLen)]

    boardScreenPositions.extend(lane6)
    boardScreenPositions.append((BOARD_START_X  + BOARD_INNER_OFFSET + posHeight/2 + posHeight*(laneLen-1), WIDTH/2 - posWidth/2))

    # lane 7 is like lane 2
    lane7 = [(BOARD_START_X + BOARD_INNER_OFFSET + posHeight/2 + i*(posHeight+1), (WIDTH/2) - posWidth - (posWidth/2)) for i in revLanes]
    boardScreenPositions.extend(lane7)

    # lane 8 is like lane 1
    lane8 = [(WIDTH/2 + 5 + posWidth - (posWidth/2), BOARD_START_Y + i*posHeight) for i in revLanes]
    boardScreenPositions.extend(lane8)


    # draw the positions
    # for i, pos in enumerate(boardScreenPositions):
        # screen.draw.text(str(i), pos, color='black')

    return boardScreenPositions

boardScreenPositions = getBoardPositions()

def getHomePathScreenPos(boardPos, playerId):

    homePathPos = abs(BOARDLENGTH - boardPos)
    print("getHomePathScreenPos: ", boardPos, playerId, homePathPos)
    
    # player 0, is between lanes 1 and 8
    if playerId == 0:
        pos = (WIDTH/2 + 5 - (posWidth/2), BOARD_START_Y + (homePathPos*posHeight))

    # between lanes 2 and 3
    elif playerId == 1:
        # pos = (BOARD_START_X + posHeight/2,WIDTH/2 - posWidth/2 + homePathPos*posWidth)
        pos = (BOARD_START_X + posHeight/2+ homePathPos*posHeight, WIDTH/2 - posHeight )

    elif playerId == 2:    
        # pos = (WIDTH/2 + 5 - (posWidth/2), BOARD_START_Y + BOARD_INNER_OFFSET - (homePathPos*posHeight))
        pos = (WIDTH/2 + 5 - (posWidth/2), BOARD_START_Y + BOARD_INNER_OFFSET*(3/2) - (homePathPos*posHeight))
    
        # pos = (WIDTH/2 + 5 - (posWidth/2), BOARD_START_Y + BOARD_INNER_OFFSET + 7*posHeight))
    elif playerId == 3:
        # pos = (BOARD_START_X  + BOARD_INNER_OFFSET + posHeight/2 + posHeight, WIDTH/2 - posWidth/2 - homePathPos*posWidth)
        pos = (BOARD_START_X  + BOARD_INNER_OFFSET*(3/2) + posHeight/2 + posHeight  - homePathPos*posHeight, WIDTH/2 - posHeight)

    else:
        pos = (0, 0)
    print("home path pos: ", pos)
    return pos

def getHomeScreenPos(playerId, pieceId):

    x = BOARD_START_X + BOARD_INNER_OFFSET*5/8 + pieceId*25
    y = BOARD_START_X + BOARD_INNER_OFFSET*5/8 + playerId*25
    return x, y

def getScreenPosition(boardPos, pieceId, playerId):
    # print("getScreenPosition ", pieceId, playerId)
    if boardPos == BASE:
        # depends on player:
        # depends on piece
        posX = BASE_SIDE_OFFSET + BASE_OFFSETS[playerId][0] + BASE_PIECE_OFFSETS[pieceId][0]
        posY = BASE_SIDE_OFFSET + BASE_OFFSETS[playerId][1] + BASE_PIECE_OFFSETS[pieceId][1]
        pos = (posX, posY)
    elif boardPos < len(boardScreenPositions):
        pos = boardScreenPositions[boardPos]
    elif boardPos > len(boardScreenPositions) and boardPos < HOME:
        # must be home path.
        pos = getHomePathScreenPos(boardPos, playerId)
    elif boardPos == HOME:
        # at home    
        pos = getHomeScreenPos(playerId, pieceId)
    else:    
        # TBF:
        pos = (500,500)    
    return pos

def drawPiece(player, piece):
    screen_pos = getScreenPosition(piece.position, piece.id, player.id)

    screen.draw.filled_circle(screen_pos, PIECE_RADIUS, SCREEN_COLORS[player.color])
    tx, ty = screen_pos
    offset = 4
    screen.draw.text(str(piece.id), (tx-offset, ty-offset), color='grey')

def on_mouse_down(pos, button):
    print("Mouse button", button, "clicked at", pos)

def draw():
    global players, board

    # screen.blit("background", (0,0))
    screen.fill((128,0,0))

    screen.blit("parcheesi_board2", (0,0))

    for p in players:
        for pc in p.pieces:
            drawPiece(p, pc)

    # draw the home paths for debugging.
    # homePathPos = 1
    # s = (WIDTH/2 + 5 - (posWidth/2), BOARD_START_Y + (homePathPos*posHeight))
    # homePathPos = 8
    # e = (WIDTH/2 + 5 - (posWidth/2), BOARD_START_Y + (homePathPos*posHeight))
    # screen.draw.line(s, e, color='black')

    # homePathPos = 1
    # pos = (BOARD_START_X + posHeight/2+ homePathPos*posHeight, WIDTH/2 - posHeight )
    # homePathPos = 8
    # e = (BOARD_START_X + posHeight/2 + homePathPos*posHeight, WIDTH/2 - posHeight )
    # screen.draw.line(pos, e, color='black')

    # homePathPos = 1
    # pos = (WIDTH/2 + 5 - (posWidth/2), BOARD_START_Y + BOARD_INNER_OFFSET*(3/2) - (homePathPos*posHeight))
    # homePathPos = 8
    # e = (WIDTH/2 + 5 - (posWidth/2), BOARD_START_Y + BOARD_INNER_OFFSET*(3/2) - (homePathPos*posHeight))
    # screen.draw.line(pos, e, color='black')
    
    # homePathPos = 1
    # pos = (BOARD_START_X  + BOARD_INNER_OFFSET*(3/2) + posHeight/2 + posHeight  - homePathPos*posHeight, WIDTH/2 - posHeight)
    # homePathPos = 8
    # e = (BOARD_START_X  + BOARD_INNER_OFFSET*(3/2) + posHeight/2 + posHeight  - homePathPos*posHeight, WIDTH/2 - posHeight)
    # screen.draw.line(pos, e, color='black')


    
def update(time_interval):
    # global bullets, tanks, rubble
    global turn, playerTurn, players, winners

    now = time.time()

    if keyboard.escape:
        sys.exit()

    rolls = None
    

    p = players[playerTurn]

        

    print("Turn %d for %s" % (turn, p))
    for pc in p.pieces:
        print("  %s" % pc)

    # players that are done don't get a turn
    if not p.allPiecesAtHome():

        # roll!
        if rolls is None:
            d1, d2 = roll()
        else:
            d1, d2 = rolls[turn]

        print(" Roll: ", d1, d2)

        # move up to two pieces!
        # first move
        moveSimple(p, d1)
        #if d1 == 5:
            # move a piece from base to start
        #    p.movePieceToStart()
        #if d2 == 5:
            # move a piece from base to start
        #    p.movePieceToStart()
        moveSimple(p, d2)    

    if p.allPiecesAtHome():
        p.rank = len(winners) + 1
        winners.append(p)

    # turn is done
    turn += 1

    playerTurn += 1
    if playerTurn > NUMPLAYERS-1:
        playerTurn = 0

    # everyone home?
    gameDone = isGameDone(players, turn, rolls)
    if gameDone:
        return

    time.sleep(.25)
    