import random
from pprint import pprint

import numpy as np
import matplotlib.pylab as plt

# one of four corners
# start (safe) - 1
# 2, 3, 4, 5
# (safe) - 6
# 7, 8, 9, 10, 11, 12
# (safe) - 13
# 13, 14, 15, 16
# start the new corner

# so the board edges are 4*16 long,
# with each player starting at base every 16 positions.
# And base starts at corner + 5
# after a plyaer has gone 4*16  - 5positions, they go up
# a home path till they get home.

# how to denote positions?  Relative to start is easy for each
# piece, but makes it hard to compare pieces from different
# players.  Instead, make absolute position primary, 
# with functions for relative position to base.

# all pieces from all players can share the same home path, so those
# will be positions > 4*16 (64)

# this means for all players but player 1, their absolute position
# will wrap around 0.  So, for player 2, they start at 16 + 5.  When 
# they get past 4*16, they restart at zero, which will be relative
# position 3*16.


#              0 (Player 1 turns into home)
#
#         5 (Player 1 start)  60
#
#      12                    53 (Player 4 start)
# 16                               48 (Player 4 turns into home)
#      21  (Player 2 start)  44
#
#          28     37 (Player 3 start)
#              32 (Player 3 turns into home)
#

# So, once any pleyaer gets past pos. 64, they restart at 0.
# once player gets past start position - 5, they jump to position 64,
# all sharing the same home path.

from Constants import *
from game import *
from Player import Player
from Piece import Piece







        # check to see if it got home
        #if pc.relativePosition() >= HOME:
        #    pc.home = True


                    

def play(numPlayers, strategy=None, rolls=None):
    
    board = {}

    # create players
    players = []
    winners = []
    for i in range(numPlayers):
        p = Player(i)
        # start al pieces off board
        # for pc in p.pieces:
            # pc.position = p.startPosition 
        print(p.getDescription())
        players.append(p)

    gameDone = False

    turn = 0
    rollIdx = 0

    while not gameDone:
        printBoard(players)
        pprint(board)

        # take turns
        for p in players:
            if gameDone:
                break

            # players that are done don't get a turn
            if p.allPiecesAtHome():
                continue

            print("Turn %d for %s" % (turn, p))
            for pc in p.pieces:
                print("  %s" % pc)

            # roll!
            doubles = 0
            rolling = True
            while rolling:

                if rolls is None:
                    d1, d2 = roll()
                else:
                    d1, d2 = rolls[rollIdx]
                    rollIdx += 1

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
                moved = movePiece(p, d1, board, strategy)
                if not moved:
                    print("%s could not move %d" % (p, d1))
                    p.blocked += 1

                moved = movePiece(p, d2, board, strategy)    
                if not moved:
                    print("%s could not move %d" % (p, d2))
                    p.blocked += 1


                    

            if p.allPiecesAtHome():
                p.rank = len(winners) + 1
                winners.append(p)

            # turn is done
            turn += 1
            p.turns += 1

            # everyone home?
            gameDone = isGameDone(players, rollIdx, rolls)
            if gameDone:
                break
        
        


    printBoard(players)

    print("Game Over")
    print("num turns: ", turn)
    print("winners: ")
    for p in players:
        print("%s" % p)
        print("  was blocked %d times" % p.blocked)
    for i, p in enumerate(winners):
        print(i+1, " : ", str(p))

    return players

def collectGameStats(strategy):
    "Play the game, and return stats"

    # play the game!
    numPlayers = 4
    players = play(numPlayers, strategy)

    # collect all the stats from the players
    winner = 0
    totalTurns = totalBlocks = totalDoubles = totalDoubleDeaths = 0
    totalDeaths = totalKills = 0

    for p in players:
        print("")
        print("%s" % p)
        print("  Finished: %d" % p.rank)
        print("  num turns: %d" % p.turns)
        print("  num kills: %d" % p.getKills())
        print("  num deaths: %d" % p.getDeaths())
        print("  num doubles: %d" % p.doubles)
        print("  num deaths by doubles: %d" % p.doubleDeaths)
        print("  was blocked %d times" % p.blocked)
        totalTurns += p.turns
        totalBlocks += p.blocked
        totalDoubles += p.doubles
        totalDoubleDeaths += p.doubleDeaths
        totalKills += p.getKills()
        totalDeaths += p.getDeaths()

        if p.rank == 1:
            winner = p

    print("")
    print("Total turns", totalTurns)
    print("Total kills", totalKills)
    print("Total deaths", totalDeaths)
    print("Total blocks", totalBlocks)
    print("Total doubles", totalDoubles)
    print("Total deaths by doubles", totalDoubleDeaths)

    gameTurns = winner.turns * numPlayers
    print("Game won after %d turns" % gameTurns)

    minPerTurn = .5

    print("Game time for %f minutes per turn: %f" % (minPerTurn, minPerTurn*gameTurns))

    stats = {
        'winTurns': gameTurns,
        'turns': totalTurns,
        'kills': totalKills,
        'deaths': totalDeaths,
        'blocks': totalBlocks,
        'doubles': totalDoubles,
        'doubleDeaths': totalDoubleDeaths,
    }

    return stats, players


def main():

    #rolls = [(5,5)]
    # play(4, rolls=rolls)
    #play(4)
    numGames = 100


    # strategy = {
    #     MAKE_KILL : 2,
    #     GET_HOME : 1,
    # }
    strategy = None

    allStats = {
        'winTurns': [],
        'turns': [],
        'kills': [],
        'deaths': [],
        'blocks': [],
        'doubles': [],
        'doubleDeaths': [],
    }

    for i in range(numGames):
        stats, players = collectGameStats(strategy)
        for k, v in stats.items():
            allStats[k].append(v)

    
    for k, v in allStats.items():
        print("%s: mean=%f, std=%f" % (k, np.mean(v), np.std(v)))    
        meanStr = "mean=%5.2f, std=%5.2f" % (np.mean(v), np.std(v))

        num_bins = 20
        n, bins, patches = plt.hist(v, num_bins, facecolor='blue', alpha=0.5)
        
        # put the stats on the plot?
        #maxV = np.max(v)
        #x = maxV - (maxV/10.)
        #print("x:",x)
        #plt.text(x, .8, meanStr, style='italic',
        #bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
        plt.xlabel(k)
        plt.ylabel("#")
        plt.title("%s from %d games (%s)" % (k, numGames, meanStr))
        plt.savefig("%s.png" % k)
        plt.show()

if __name__ == '__main__':
    main()