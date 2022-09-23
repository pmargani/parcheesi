import time
import sys
import random

import pygame

from Constants import *
from game import *
from Player import Player

WIDTH = 600
HEIGHT = 800

STATUS_HEIGHT = 250

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
d1 = d2 = None
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

def makePiecePositionOffset(i, pos, screenPos, playerId):

    if i == 0:
        return screenPos

    offset = PIECE_RADIUS*2
    x, y = screenPos

    if pos >= 0 and pos < BOARDLENGTH/8:
        xOff = i*offset
        yOff = 0
    elif pos >= BOARDLENGTH/8 and pos < (BOARDLENGTH*3)/8:
        xOff = 0
        yOff = i*offset      
    elif pos >= (BOARDLENGTH*3)/8 and pos < (BOARDLENGTH*5)/8:
        xOff = i*offset
        yOff = 0
    elif pos >= (BOARDLENGTH*5)/8 and pos < (BOARDLENGTH*7)/8:
        xOff = 0
        yOff = i*offset
    elif pos < BOARDLENGTH:
        xOff = i*offset
        yOff = 0
    elif pos >= BOARDLENGTH:
        if playerId in [0, 2]:
            xOff = i*offset
            yOff = 0
        else:        
            xOff = 0
            yOff = i*offset

    return x + xOff, y + yOff
            
def drawPiece(player, piece, board):
    screen_pos = getScreenPosition(piece.position, piece.id, player.id)

    if piece.position != BASE and piece.position < HOME:
        # how many other pieces on this position?
        for i, pc in enumerate(board[piece.position]):
            if pc == piece:
                break

        screen_pos = makePiecePositionOffset(i, piece.position, screen_pos, player.id)
    
    screen.draw.filled_circle(screen_pos, PIECE_RADIUS, SCREEN_COLORS[player.color])
    tx, ty = screen_pos
    offset = 4
    screen.draw.text(str(piece.id), (tx-offset, ty-offset), color='grey')

def on_mouse_down(pos, button):
    print("Mouse button", button, "clicked at", pos)

def draw():
    global players, board, d1, d2

    # screen.blit("background", (0,0))
    screen.fill((128,0,0))

    screen.blit("parcheesi_board2", (0,0))

    row = 0
    yBase = HEIGHT - STATUS_HEIGHT 
    yStep = 20
    screen.draw.text("Roll: %d %d" % (d1, d2), (0, yBase))

    for p in players:

        for pc in p.pieces:
            drawPiece(p, pc, board)

        x = (WIDTH/4) * p.id
        row = 1
        pos = (x, yBase + (row*yStep))
        screen.draw.text("Player %d" % p.id, pos)

        row += 1
        screen.draw.text("Rank: %s" % p.rank, (x, yBase+(yStep*row)), fontsize=16)
        
        row += 1
        screen.draw.text("Kills: %d" % p.getKills(), (x, yBase+(yStep*row)), fontsize=16)

        row += 1
        screen.draw.text("Deaths: %d" % p.getDeaths(), (x, yBase+(yStep*row)), fontsize=16)
        
        row += 1
        screen.draw.text("Blocked: %d" % p.blocked, (x, yBase+(yStep*row)), fontsize=16)

        row += 1
        screen.draw.text("Turns: %d" % p.turns, (x, yBase+(yStep*row)), fontsize=16)

        row += 1
        screen.draw.text("Doubles: %d" % p.doubles, (x, yBase+(yStep*row)), fontsize=16)

        row += 1
        screen.draw.text("Dbl Deaths: %d" % p.doubleDeaths, (x, yBase+(yStep*row)), fontsize=16)

        for pc in p.pieces:
            row += 1
            pos = (x, yBase+(yStep*row))
            txt = "PC %d Pos: %d K: %d D: %d" % (pc.id, pc.position, pc.kills, pc.deaths)
            screen.draw.text(txt, pos, fontsize=16) 

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
    global turn, playerTurn, players, winners, d1, d2

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

        doubles = 0
        rolling = True
        while rolling: 
            # roll!
            if rolls is None:
                d1, d2 = roll()
            else:
                d1, d2 = rolls[turn]

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
                    print("Third doubles!", d1, d2)
                    loseBestPiece(p, board)
                    p.doubleDeaths += 1
                    rolling = False
                    break

            # move up to two pieces!
            # first move
            moved = moveLegal(p, d1, board)
            if not moved:
                print("%s could not move %d" % (p, d1))
                p.blocked += 1

            moved = moveLegal(p, d2, board)    
            if not moved:
                print("%s could not move %d" % (p, d1))
                p.blocked += 1

    if p.allPiecesAtHome():
        if p.rank is None:
            p.rank = len(winners) + 1
            winners.append(p)

    # turn is done
    turn += 1
    p.turns += 1

    playerTurn += 1
    if playerTurn > NUMPLAYERS-1:
        playerTurn = 0

    # everyone home?
    gameDone = isGameDone(players, turn, rolls)
    if gameDone:
        return

    time.sleep(.25)
    # x = input()
    