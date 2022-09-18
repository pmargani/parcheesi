import unittest

from Constants import *
from main import play

class TestMain(unittest.TestCase):

    def test_play1(self):
        "One player gets two pieces out"

        s = START_ROLL
        rolls = [(s,s)]

        players = play(1, rolls=rolls)

        # first 2 pieces will be on start, others at base
        pos = [STARTOFFSET, STARTOFFSET, BASE, BASE]
        p0 = players[0]
        for i in range(len(pos)):
            self.assertEqual(pos[i], p0.pieces[i].position)

    def test_play2(self):
        "One player advances one piece"

        s = START_ROLL
        rolls = [(s,s),(1,2)]

        players = play(1, rolls=rolls)

        pos = [STARTOFFSET + 3, STARTOFFSET, BASE, BASE]
        p0 = players[0]
        for i in range(len(pos)):
            self.assertEqual(pos[i], p0.pieces[i].position)          

    def test_play3(self):
        "One player gets one piece home"

        s = START_ROLL
        sixes = (6, 6)
        rolls = [(s,6),sixes, sixes, sixes, sixes, sixes, sixes]

        players = play(1, rolls=rolls)

        pos = [HOME, BASE, BASE, BASE]
        p0 = players[0]
        for i in range(len(pos)):
            self.assertEqual(pos[i], p0.pieces[i].position)

    def test_play4(self):
        "One player gets one piece home and moves a second piece"

        s = START_ROLL
        sixes = (6, 6)
        rolls = [(s,s)]
        rolls.extend([sixes]*7)

        players = play(1, rolls=rolls)

        pos = [HOME, STARTOFFSET+12, BASE, BASE]
        p0 = players[0]
        for i in range(len(pos)):
            self.assertEqual(pos[i], p0.pieces[i].position)
    
    def test_play5(self):
        "4 players move identically"

        s = START_ROLL
        ss = (s,s)
        sixes = (6, 6)
        rolls = [ss, ss, ss, ss, sixes, sixes, sixes, sixes]

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


if __name__ == '__main__':
    unittest.main()            