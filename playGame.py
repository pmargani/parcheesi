import time
import sys

import pygame

from Constants import *
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
    (bo, 0),
    (bo, bo),
    (0, bo)

]

po = 25
BASE_PIECE_OFFSETS = [
    (0, 0),
    (po, 0),
    (po, po),
    (0, po)
]

players = []
winners = []
for i in range(NUMPLAYERS):
    p = Player(i)
    # start al pieces off board
    # for pc in p.pieces:
        # pc.position = p.startPosition 
    print(p.getDescription())
    players.append(p)

def getScreenPosition(boardPos, pieceId, playerId):
    print("getScreenPosition ", pieceId, playerId)
    if boardPos == BASE:
        # depends on player:
        # depends on piece
        posX = BASE_SIDE_OFFSET + BASE_OFFSETS[playerId][0] + BASE_PIECE_OFFSETS[pieceId][0]
        posY = BASE_SIDE_OFFSET + BASE_OFFSETS[playerId][1] + BASE_PIECE_OFFSETS[pieceId][1]
        pos = (posX, posY)
    else:    
        pos = (500, 500)
    return pos

def drawPiece(player, piece):
    screen_pos = getScreenPosition(piece.position, piece.id, player.id)

    screen.draw.filled_circle(screen_pos, PIECE_RADIUS, SCREEN_COLORS[player.color])
    tx, ty = screen_pos
    offset = 4
    screen.draw.text(str(piece.id), (tx-offset, ty-offset), color='grey')

def draw():
    global players

    # screen.blit("background", (0,0))
    screen.fill((128,0,0))

    screen.blit("parcheesi_board2", (0,0))

    for p in players:
        for pc in p.pieces:
            drawPiece(p, pc)



def update(time_interval):
    # global bullets, tanks, rubble

    now = time.time()

    if keyboard.escape:
        sys.exit()
