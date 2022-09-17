import unittest

from Constants import *
from Piece import Piece
from Player import Player

class TestPiece(unittest.TestCase):

    def test_piecePlayer0(self):
        p = Player(0 , 'color')
        pc = Piece(0, p)

        self.assertEqual(0, pc.id)

        self.assertTrue(pc.atBase())    
        self.assertFalse(pc.atHome())   
        self.assertFalse(pc.isOnBoard())    

        self.assertEqual(pc.startPosition, 5)
        self.assertEqual(pc.homePathStartPosition, 0)

        # get it started
        start = pc.startPosition
        pc.position = start

        self.assertEqual(pc.advancePosition(12), start + 12)
        self.assertEqual(pc.advancePosition(12), start + 12*2)
        self.assertEqual(pc.advancePosition(12), start+(12*3))
        self.assertEqual(pc.advancePosition(12), start+(12*4)) # 53
        self.assertEqual(pc.advancePosition(8), 61)
        self.assertEqual(pc.advancePosition(10), 71)

    def test_piecePlayer1(self):
        p = Player(1 , 'color')
        pc = Piece(0, p)

        self.assertEqual(0, pc.id)

        self.assertTrue(pc.atBase())    
        self.assertFalse(pc.atHome())   
        self.assertFalse(pc.isOnBoard())    

        self.assertEqual(pc.startPosition, 22)
        self.assertEqual(pc.homePathStartPosition, 17)

        # get it started
        start = p.startPosition
        pc.position = start

        self.assertEqual(pc.advancePosition(12), start+12)
        self.assertEqual(pc.advancePosition(12), start+12+12)
        self.assertEqual(pc.advancePosition(12), start+(12*3)) # 58
        self.assertEqual(pc.advancePosition(12), 2) # 70 - 68 
        self.assertEqual(pc.advancePosition(12), 14)
        self.assertEqual(pc.advancePosition(5), 70)
        self.assertEqual(pc.advancePosition(2), 72)
        self.assertEqual(pc.advancePosition(12), HOME)
        self.assertEqual(pc.advancePosition(12), HOME)

    def test_piecePlayer2(self):
        p = Player(2 , 'color')
        pc = Piece(0, p)

        self.assertEqual(0, pc.id)

        self.assertTrue(pc.atBase())    
        self.assertFalse(pc.atHome())   
        self.assertFalse(pc.isOnBoard())    

        self.assertEqual(pc.homePathStartPosition, 2*17)
        self.assertEqual(pc.startPosition, 2*17 + 5)

       # get it started
        start = p.startPosition
        pc.position = start

        self.assertEqual(pc.advancePosition(12), start+12) # 51
        self.assertEqual(pc.advancePosition(12), start+12+12) # 63
        self.assertEqual(pc.advancePosition(12),  7)
        self.assertEqual(pc.advancePosition(12), 19) # 
        self.assertEqual(pc.advancePosition(12), 31)
        self.assertEqual(pc.advancePosition(5), 70)
        self.assertEqual(pc.advancePosition(2), 72)
        self.assertEqual(pc.advancePosition(12), HOME)



    def test_piecePlayer3(self):
        p = Player(3, 'color')
        pc = Piece(0, p)

        self.assertEqual(0, pc.id)

        self.assertTrue(pc.atBase())    
        self.assertFalse(pc.atHome())   
        self.assertFalse(pc.isOnBoard())    

        self.assertEqual(pc.homePathStartPosition, 3*17)
        self.assertEqual(pc.startPosition, 3*17 + 5)

       # get it started
        start = p.startPosition
        pc.position = start

        # avoid landing on zero!
        self.assertEqual(pc.advancePosition(11), start+11) # 56 + 12 = 68
        self.assertEqual(pc.advancePosition(12), 11) # 63
        self.assertEqual(pc.advancePosition(12), 23)
        self.assertEqual(pc.advancePosition(12), 35) # 
        self.assertEqual(pc.advancePosition(12), 47)
        self.assertEqual(pc.advancePosition(5), 69)
        self.assertEqual(pc.advancePosition(2), 71)
        self.assertEqual(pc.advancePosition(12), HOME)

if __name__ == '__main__':
    unittest.main()
