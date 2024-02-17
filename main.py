import random
import argparse
from pprint import pprint

import numpy as np
import matplotlib.pylab as plt

from ParcheesiGame import ParcheesiGame
from Constants import *

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


def collectGameStats(strategy, verbose=False):
    "Play the game, and return stats"

    # play the game!
    numPlayers = 4
    game = ParcheesiGame(numPlayers, strategy=strategy, verbosity=verbose)
    game.play()
    players = game.players

    #players = play(numPlayers, strategy, verbose=verbose)

    # collect all the stats from the players
    winner = 0
    totalTurns = totalBlocks = totalDoubles = totalDoubleDeaths = 0
    totalDeaths = totalKills = 0

    for p in players:
        if verbose:
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

    if verbose:
        print("")
        print("Total turns", totalTurns)
        print("Total kills", totalKills)
        print("Total deaths", totalDeaths)
        print("Total blocks", totalBlocks)
        print("Total doubles", totalDoubles)
        print("Total deaths by doubles", totalDoubleDeaths)

    gameTurns = winner.turns * numPlayers
    minPerTurn = .5

    if verbose:
        print("Game won after %d turns" % gameTurns)
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


def runGames(numGames, strategyName=None, plot=True, verbose=False):
    "Top level entry point for running experiment with multiple games"

    # manage strategies
    if strategyName in STRATEGIES:
        strategy = STRATEGIES[strategyName]
    else:
        strategy = None

    # init stats
    # TBF: make this a class?
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
        stats, players = collectGameStats(strategy, verbose=verbose)
        for k, v in stats.items():
            allStats[k].append(v)

    
    for k, v in allStats.items():
        if verbose:
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
        if not plot:
            continue

        plt.xlabel(k)
        plt.ylabel("#")
        plt.title("%s from %d games (%s)" % (k, numGames, meanStr))
        plt.savefig("%s.png" % k)
        plt.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--numGames", help="number of games to run in the simulation", type=int, default=100)
    parser.add_argument("--strategy", help="name of strategy to play game with", type=str, default=None)
    parser.add_argument("--plot", help="plot results?", action='store_true')
    parser.add_argument("--verbose", help="print results?", action='store_true')
    args = parser.parse_args()

    print(f"numGames: {args.numGames}")
    print(f"plot: {args.plot}")
    print(f"verbose: {args.verbose}")
    print(f"strategy name: {args.strategy}")

    strategyNames = ",".join(STRATEGIES.keys())

    valid = True
    if args.numGames < 1:
        print(f"ERROR: you must play one or more games")
        valid = False
    if args.strategy is not None and args.strategy not in STRATEGIES:
        print(f"ERROR: strategy {args.strategy} not in list {strategyNames}")    
        valid = False

    if valid:
        runGames(args.numGames, plot=args.plot, verbose=args.verbose)

    print(f"Parcheesi Game Simulations Complete")
    
if __name__ == '__main__':
    main()