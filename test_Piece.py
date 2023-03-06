import unittest

from Constants import *
from Piece import Piece
from Player import Player

class TestPiece(unittest.TestCase):

    def test_Piece(self):
        p0 = Player(0 , 'color')
        pc0 = Piece(0, p0)
        pc02 = Piece(0, p0)

        self.assertEqual(pc0, pc02)

        # p = Player(0 , 'color')
        pc1 = Piece(1, p0)        
        self.assertNotEqual(pc0, pc1)

        p1 = Player(1 , 'color')
        pc01 = Piece(0, p1)
        self.assertNotEqual(pc0, pc01)

        self.assertTrue(pc0.atBase())    
        self.assertFalse(pc0.atHome())   
        self.assertFalse(pc0.isOnBoard())
        self.assertFalse(pc0.isOnMainBoard())
        
        self.assertEqual(pc0.distanceFromStart(), 0)

        # move piece around and tst stuff
        pc0.position = pc0.startPosition

        self.assertFalse(pc0.atBase())    
        self.assertFalse(pc0.atHome())   
        self.assertTrue(pc0.isOnBoard())
        self.assertTrue(pc0.isOnMainBoard())
        self.assertEqual(pc0.distanceFromStart(), 0)
        
        pc0.position += 1

        self.assertFalse(pc0.atBase())    
        self.assertFalse(pc0.atHome())   
        self.assertTrue(pc0.isOnBoard())
        self.assertTrue(pc0.isOnMainBoard())
        self.assertEqual(pc0.distanceFromStart(), 1)

        # keep it on main board
        nextPos = BOARDLENGTH - pc0.startPosition - 2
        pc0.position += nextPos
        # print("pc0.position:   ", pc0.position, pc0.position - pc0.startPosition)

        self.assertFalse(pc0.atBase())    
        self.assertFalse(pc0.atHome())   
        self.assertFalse(pc0.isInHomePath())   
        self.assertTrue(pc0.isOnBoard())
        self.assertTrue(pc0.isOnMainBoard())
        self.assertEqual(pc0.distanceFromStart(), nextPos + 1)
               
        # now get into home path
        pc0.position += 3

        self.assertFalse(pc0.atBase())    
        self.assertFalse(pc0.atHome())   
        self.assertTrue(pc0.isInHomePath())   
        self.assertTrue(pc0.isOnBoard())
        self.assertFalse(pc0.isOnMainBoard())
        self.assertEqual(pc0.distanceFromStart(), nextPos + 1 + 3)

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
        # need exact step
        self.assertEqual(pc.advancePosition(4), HOME)
        # self.assertEqual(pc.advancePosition(12), HOME)

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
        # can't move!
        self.assertEqual(pc.advancePosition(6), 72)
        # need exact roll
        self.assertEqual(pc.advancePosition(4), HOME)



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
        self.assertEqual(pc.advancePosition(5), HOME)


    def test_pieceStart(self):

        p = Player(3, 'color')
        pc = Piece(0, p)

        self.assertEqual(0, pc.id)

        self.assertEqual(pc.startPosition, pc.getNextPosition(START_ROLL))

if __name__ == '__main__':
    unittest.main()
