from Constants import *
from Piece import Piece

class Player:

    def __init__(self, id, color=None):

        self.id = id
        if color is not None:
            self.color = color
        else:
            self.color = COLORS[self.id]

        self.homePathStartPosition = self.id * BASEOFFSET
        self.startPosition = self.homePathStartPosition + STARTOFFSET

        self.pieces = [Piece(0, self), Piece(1, self), Piece(2, self), Piece(3, self)]

        self.rank = None
        
    def __str__(self):
        return "Player %d (%s)" % (self.id, self.color)

    def getDescription(self):
        s = "Player %d (%s) starts pieces at %d, and pieces go home at %d\n" % (self.id, self.color, self.startPosition, self.homePathStartPosition)
        for pc in self.pieces:
            s += "  Piece: %s\n" % pc
        return s
            
    def movePieceToStart(self):
        "move the first piece at base you come across and move it on the board"
        for p in self.pieces:
            if p.position == BASE:
                print("moving %s to start" % p)
                p.position = self.startPosition
                break

    def allPiecesAtHome(self):
        "Are all four pieces at home"
        for p in self.pieces:
            if not p.atHome():
                return False
        return True