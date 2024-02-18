from datetime import datetime
import argparse
import pickle

import numpy as np
import matplotlib.pylab as plt

from ParcheesiGame import ParcheesiGame
from Stats import Stats
from Constants import *



class Experiment:

    """
    A class for playing Parcheesi N times with a given 
    strategy and reporting on the results.
    """

    def __init__(self, experimentName, numGames, numPlayers, save=False, strategy=None, verbosity=None):

        self.verbosity = 0
        if verbosity is not None:
            self.verbosity = verbosity
        
        self.save = save
        self.expName = experimentName
        self.numGames = numGames
        self.numPlayers = numPlayers

        # manage strategies
        self.strategyName = strategy
        if strategy in STRATEGIES:
            self.strategy = STRATEGIES[strategy]
        else:
            self.strategy = None

        # init stats
        self.expStats = Stats(self.numGames)
        self.playerStats = []
        for i in range(self.numPlayers):
            self.playerStats.append(Stats(self.numGames))
        
        # plotting
        self.numBinsPlot = 20

    def __str__(self):
        s = f"""
        Experiment {self.expName}:
          numGames: {self.numGames}
          numPlayers: {self.numPlayers}
          strategy: {self.strategyName}
        """  
        return s

    def run(self):
        "Run the experiment - play the game N times and report results"

        for igame in range(self.numGames):
            g = ParcheesiGame(
                self.numPlayers, 
                strategy=self.strategy, 
                verbosity=self.verbosity
            )
            g.play()

            # collect stats
            self.expStats.winTurns[igame] = g.winTurns
            self.expStats.turns[igame] = g.turns
            self.expStats.kills[igame] = g.kills
            self.expStats.deaths[igame] = g.deaths
            self.expStats.doubleDeaths[igame] = g.doubleDeaths
            self.expStats.doubles[igame] = g.deaths
            self.expStats.blocks[igame] = g.blocks

        if self.verbosity > 0:
            print("Experiment stats:")
            print("Num games: %d" % self.numGames)
            self.printStats("winTurns", self.expStats.winTurns)
            self.printStats("turns", self.expStats.turns)
            self.printStats("blocks", self.expStats.blocks)
            self.printStats("deaths", self.expStats.deaths)
            self.printStats("kills", self.expStats.kills)
            self.printStats("doubles", self.expStats.doubles)
            self.printStats("doubleDeaths", self.expStats.doubleDeaths)

        self.plotResults()

        # if self.save:
            # self.saveResults()

    # TBF: seem to be problems pickling an object from itself?
    # def saveResults(self):
    #     "Persist the results via pickle"
    #     pass

    #     nowStr = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    #     fn = "%s.%s.pkl" % (self.expName, nowStr)
    #     with open(fn, 'wb') as f:
    #         pickle.dump(self, f)
   
    #     if self.verbosity > 0:
    #         print("Pickled Experiment to: %s" % fn)

    def plotResults(self, show=False):
        "Make plots from the experiment"

        self.plotResult("winTurns", self.expStats.winTurns,show=show)
        self.plotResult("turns", self.expStats.turns,show=show)
        self.plotResult("blocks", self.expStats.blocks,show=show)
        self.plotResult("deaths", self.expStats.deaths,show=show)
        self.plotResult("kills", self.expStats.kills,show=show)
        self.plotResult("doubles", self.expStats.doubles,show=show)
        self.plotResult("doubleDeaths", self.expStats.doubleDeaths,show=show)

    def plotResult(self, name, v, show=False):
        "Make a historgram plot of the given result"

        meanStr = "mean=%5.2f, std=%5.2f" % (np.mean(v), np.std(v))

        n, bins, patches = plt.hist(v, self.numBinsPlot, facecolor='blue', alpha=0.5)

        plt.xlabel(name)
        plt.ylabel("#")
        plt.title("%s from %d games (%s)" % (name, self.numGames, meanStr))
        
        if self.save:
            plt.savefig("%s_%s.png" % (self.expName, name))

        if self.verbosity > 0 or show:
            plt.show()        

    def printStats(self, name, xs):
        "print the stats of the given data"
        print("%s mean=%5.2f std=%5.2f" % (name, np.mean(xs), np.std(xs)))

def runExperiment(name, numGames, numPlayers, strategy=None, verbosity=0, save=False):
    exp = Experiment(name, numGames, numPlayers, strategy=strategy, verbosity=verbosity, save=save)
    exp.run()

    if save:
        print("saving here")
        nowStr = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        fn = "%s.%s.pkl" % (exp.expName, nowStr)
        with open(fn, 'wb') as f:
            pickle.dump(exp, f)
   
        if verbosity > 0:
            print("Pickled Experiment to: %s" % fn)  

        # with open(fn, 'rb') as f:
        #     d = pickle.load(f)

        # print("loaded!")    

def loadExperiment(fn):

        with open(fn, 'rb') as f:
            e = pickle.load(f)

        print(f"loaded experiment {fn}")  
        print(e)
        e.plotResults(show=True)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="name of this experiment to run or load")
    parser.add_argument("--load", help="load named experiment", action='store_true')
    parser.add_argument("--numGames", help="number of games to run in the simulation", type=int, default=100)
    parser.add_argument("--numPlayers", help="number of players in the simulation", type=int, default=4)
    parser.add_argument("--strategy", help="name of strategy to play game with", type=str, default=None)
    parser.add_argument("--save", help="sav results?", action='store_true')
    parser.add_argument("--verbose", help="print results?", action='store_true')
    args = parser.parse_args()

    print(f"numGames: {args.numGames}")
    print(f"save: {args.save}")
    print(f"verbose: {args.verbose}")
    print(f"strategy name: {args.strategy}")
    print(f"load experiment: {args.load}")

    strategyNames = ",".join(STRATEGIES.keys())
    v = 1 if args.verbose else 0

    valid = True
    if args.numGames < 1:
        print(f"ERROR: you must play one or more games")
        valid = False
    if args.numPlayers < 2 or args.numPlayers > 4:
        print(f"ERROR: you must have 2, 3, or 4 players")
        valid = False

    if args.strategy is not None and args.strategy not in STRATEGIES:
        print(f"ERROR: strategy {args.strategy} not in list {strategyNames}")    
        valid = False
    # simple tests
    # numGames = 100
    # numPlayers = 4

    if args.load:
        loadExperiment(args.name)
    else:    
        runExperiment(args.name, args.numGames, args.numPlayers, strategy=args.strategy, verbosity=v, save=args.save)
  
    print(f"Experiment {args.name} Complete")

if __name__ == "__main__":
    main()        
