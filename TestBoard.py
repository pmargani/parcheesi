import unittest

from Constants import *
from Piece import Piece
from Player import Player
from Board import Board
from game import isMoveLegal

class TestBoard(unittest.TestCase):

    def setUp(self):

        # create players
        self.numPlayers = 4
        self.players = []
        for i in range(self.numPlayers):
            p = Player(i)
            self.players.append(p)

    def test1(self):
        "test various simple scenarios"
        b = Board()
        ps = self.players
        p0 = ps[0]
        pc0 = p0.pieces[0]

        self.assertEqual(0, b.numPiecesOnBoard())
        for i, p in enumerate(ps):
            # better be open
            self.assertTrue(b.isStartOpen(p))
            # better not be any thing on the board yet
            pos = i*BASEOFFSET + STARTOFFSET
            self.assertEqual(0, b.numPiecesOnBoardPos(pos, p.pieces[0]))
            self.assertFalse(b.isOccupiedByPlayer(pos, p))
            self.assertFalse(b.isOccupiedByOtherPlayer(pos, p))

        # put each piece at it's own start
        for i, p in enumerate(ps):
            # note we have to change both piece and board
            pos = i*BASEOFFSET + STARTOFFSET
            p.pieces[0].position = pos
            b.movePieceToStart(p.pieces[0])

        b.printBoard(ps)
        print(b.board)

        self.assertEqual(self.numPlayers, b.numPiecesOnBoard())
        for i, p in enumerate(ps):
            # better be open
            self.assertTrue(b.isStartOpen(p))
            # better not be any thing on the board yet
            pos = i*BASEOFFSET + STARTOFFSET
            self.assertEqual(1, b.numPiecesOnBoardPos(pos, p.pieces[0]))
            self.assertTrue(b.isOccupiedByPlayer(pos, p))
            self.assertFalse(b.isOccupiedByOtherPlayer(pos, p))

        # put a second piece at it's own start
        for i, p in enumerate(ps):
            # note we have to change both piece and board
            pos = i*BASEOFFSET + STARTOFFSET
            p.pieces[1].position = pos
            b.movePieceToStart(p.pieces[1])

        self.assertEqual(2*self.numPlayers, b.numPiecesOnBoard())
        for i, p in enumerate(ps):
            # better be open
            self.assertFalse(b.isStartOpen(p))
            # better not be any thing on the board yet
            pos = i*BASEOFFSET + STARTOFFSET
            self.assertEqual(2, b.numPiecesOnBoardPos(pos, p.pieces[0]))
            self.assertTrue(b.isOccupiedByPlayer(pos, p))
            self.assertFalse(b.isOccupiedByOtherPlayer(pos, p))
            

        # move first players piece forward,
        # then add another of it's pieces to start
        p0.pieces[0].position = STARTOFFSET + 1
        b.update(p0.pieces[0], STARTOFFSET, STARTOFFSET + 1)
        p0.pieces[2].position = STARTOFFSET 
        b.movePieceToStart(p0.pieces[2])

        # we added one to the field
        self.assertEqual(2*self.numPlayers+1, b.numPiecesOnBoard())
        # but none of this has changed!
        for i, p in enumerate(ps):
            # better be open
            self.assertFalse(b.isStartOpen(p))
            # better not be any thing on the board yet
            pos = i*BASEOFFSET + STARTOFFSET
            self.assertEqual(2, b.numPiecesOnBoardPos(pos, p.pieces[0]))
            self.assertTrue(b.isOccupiedByPlayer(pos, p))
            self.assertFalse(b.isOccupiedByOtherPlayer(pos, p))
        # check advanced piece
        pos = STARTOFFSET + 1
        self.assertEqual(1, b.numPiecesOnBoardPos(pos, p0.pieces[0]))
        self.assertTrue(b.isOccupiedByPlayer(pos, p0))
        self.assertFalse(b.isOccupiedByOtherPlayer(pos, p0))
        # how about from the other player's perspective?
        self.assertFalse(b.isOccupiedByPlayer(pos, ps[1]))
        self.assertTrue(b.isOccupiedByOtherPlayer(pos, ps[1]))
     

    # def test_isMoveLegal(self):

    #     p0 = Player(0 , 'color')
    #     pc0 = Piece(0, p0)
    #     board = {}

    #     # a 5 should get this piece out of base into it's start
    #     l = isMoveLegal(pc0, 5, board)
    #     self.assertTrue(l)

    #     # but this role doesn't work
    #     l = isMoveLegal(pc0, 1, board)
    #     self.assertFalse(l)

if __name__ == '__main__':
    unittest.main()