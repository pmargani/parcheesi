import unittest

from Constants import *
from Piece import Piece
from Player import Player
from Board import Board
from game import isMoveLegal

class TestGame(unittest.TestCase):

    def test_isMoveLegal(self):

        p0 = Player(0 , 'color')
        pc0 = Piece(0, p0)
        board = Board()

        # a 5 should get this piece out of base into it's start
        l = isMoveLegal(pc0, 5, board)
        self.assertTrue(l)

        # but this role doesn't work
        l = isMoveLegal(pc0, 1, board)
        self.assertFalse(l)

if __name__ == '__main__':
    unittest.main()