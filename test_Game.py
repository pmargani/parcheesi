import unittest

from Constants import *
from Piece import Piece
from Player import Player
from Board import Board
from game import isMoveLegal
from game import play 

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

    def test_play1(self):
        "One player gets two pieces out with doubles"

        s = START_ROLL
        rolls = [(s,s),(1,2)]

        players = play(1, rolls=rolls)

        # first 2 pieces will be on start, others at base
        pos = [STARTOFFSET+3, STARTOFFSET, BASE, BASE]
        p0 = players[0]
        for i in range(len(pos)):
            self.assertEqual(pos[i], p0.pieces[i].position)

    def test_play1strategy1(self):
        "One player gets two pieces out with doubles"

        # using this simple strategy should give same result as
        # default 'strategy'
        strategy = {
            START_PIECE: 2,
            GET_HOME: 1
        }
        s = START_ROLL
        rolls = [(s,s),(1,2)]

        players = play(1, strategy=strategy, rolls=rolls)

        # first 2 pieces will be on start, others at base
        pos = [STARTOFFSET+3, STARTOFFSET, BASE, BASE]
        p0 = players[0]
        for i in range(len(pos)):
            self.assertEqual(pos[i], p0.pieces[i].position)

    def test_play2(self):
        "One player advances one piece"

        s = START_ROLL
        rolls = [(s,s),(1,2),(1,2)]

        players = play(1, rolls=rolls)

        pos = [STARTOFFSET + 6, STARTOFFSET, BASE, BASE]
        p0 = players[0]
        for i in range(len(pos)):
            self.assertEqual(pos[i], p0.pieces[i].position)          

    def test_play3(self):
        "One player gets one piece home"

        s = START_ROLL
        sixes = (6, 4)
        rolls = [(s,6)]
        rolls.extend([sixes]*10) #,sixes, sixes, sixes, sixes, sixes, sixes]

        players = play(1, rolls=rolls)

        pos = [HOME, BASE, BASE, BASE]
        p0 = players[0]
        for i in range(len(pos)):
            self.assertEqual(pos[i], p0.pieces[i].position)

    def test_play4(self):
        "One player gets one piece home and moves a second piece"

        s = START_ROLL
        sixes = (6, 4)
        rolls = [(s,6),(s,6)]
        rolls.extend([sixes]*5)
        rolls.append((3,4))
        rolls.append((2,4))

        players = play(1, rolls=rolls)

        pos = [HOME, STARTOFFSET+4, BASE, BASE]
        p0 = players[0]
        for i in range(len(pos)):
            print("Piece %s" % p0.pieces[i])
            self.assertEqual(pos[i], p0.pieces[i].position)
    
    def test_play5(self):
        "4 players move identically"

        s = START_ROLL
        ss = (s,6)
        sixes = (6, 4)
        # rolls = [ss, ss, ss, ss, sixes, sixes, sixes, sixes]
        rolls = [ss] * 8

        players = play(4, rolls=rolls)
        rolls
        pos = [STARTOFFSET + 12, STARTOFFSET, BASE, BASE]
        for p in players:
            o = p.id * BASEOFFSET
            for i in range(len(pos)):
                if pos[i] != BASE:
                    self.assertEqual(pos[i]+o, p.pieces[i].position)
                else:    
                    self.assertEqual(pos[i], p.pieces[i].position)

    def test_play6(self):
        "1 player blocks itself"

        s = START_ROLL
        rolls = [(s,6),(s,6),(s,6),(s,6)]

        players = play(1, rolls=rolls)

        pos = [STARTOFFSET + 6*4 + 5, STARTOFFSET, STARTOFFSET, BASE]
        p0 = players[0]
        for i in range(len(pos)):
            self.assertEqual(pos[i], p0.pieces[i].position)

    def test_play6strategy1(self):
        "1 player blocks itself"

        # using this simple strategy should give same result as
        # default 'strategy'
        strategy = {
            START_PIECE: 2,
            GET_HOME: 1
        }

        s = START_ROLL
        rolls = [(s,6),(s,6),(s,6),(s,6)]

        players = play(1, rolls=rolls)

        pos = [STARTOFFSET + 6*4 + 5, STARTOFFSET, STARTOFFSET, BASE]
        p0 = players[0]
        for i in range(len(pos)):
            self.assertEqual(pos[i], p0.pieces[i].position)

    def test_play6strategy2(self):
        "1 player blocks itself"

        # using this simple strategy should give same result as
        # default 'strategy'
        strategy = {
            MOVE_FORWARD: 2,
            GET_HOME: 1
        }

        s = START_ROLL
        rolls = [(s,6),(s,6),(s,6),(s,6)]

        players = play(1, rolls=rolls)

        pos = [STARTOFFSET + 6*4 + 5, STARTOFFSET, STARTOFFSET, BASE]
        p0 = players[0]
        for i in range(len(pos)):
            self.assertEqual(pos[i], p0.pieces[i].position)

    def test_play7(self):
        "Player 2 blocks Player 1"

        s = START_ROLL
        # player 1 gets a piece out and tries to advance
        p0rolls = [(s,6),(1,2),(1,2),(1,2),(4,6),(4,6)]
        # player 2 gets all it's pieces out, and current algorithm
        # keeps two pieces at it's start
        p1rolls = [(s,1),(s,1),(s,1),(1,2),(1,2),(1,2)]
        rolls = []
        for i in range(len(p0rolls)):
            rolls.append(p0rolls[i])
            rolls.append(p1rolls[i])

        players = play(2, rolls=rolls)
        
        # for p in players:
        #     print("%s" % p)
        #     for pc in p.pieces:
        #         print("%s" % pc)

        # see how player1 couldn't get past player2's start
        pos = [20, BASE, BASE, BASE]
        p0 = players[0]
        for i in range(len(pos)):
            self.assertEqual(pos[i], p0.pieces[i].position)   

        self.assertEqual(p0.blocked, 4)


if __name__ == '__main__':
    unittest.main()