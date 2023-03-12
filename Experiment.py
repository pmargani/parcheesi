from datetime import datetime
import pickle

import numpy as np
import matplotlib.pylab as plt

from ParcheesiGame import ParcheesiGame
from Stats import Stats



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

        # init stats
        self.expStats = Stats(self.numGames)
        self.playerStats = []
        for i in range(self.numPlayers):
            self.playerStats.append(Stats(self.numGames))
        
        # plotting
        self.numBinsPlot = 20

    def run(self):
        "Run the experiment - play the game N times and report results"

        for igame in range(self.numGames):
            g = ParcheesiGame(self.numPlayers, verbosity=self.verbosity)
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

        if self.save:
            self.saveResults()

    def saveResults(self):
        "Persist the results via pickle"

        nowStr = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        fn = "%s.%s.pkl" % (self.expName, nowStr)
        with open(fn, 'wb') as f:
            pickle.dump(self, f)
   
        if self.verbosity > 0:
            print("Pickled Experiment to: %s" % fn)

    def plotResults(self):
        "Make plots from the experiment"

        self.plotResult("winTurns", self.expStats.winTurns)
        self.plotResult("turns", self.expStats.turns)
        self.plotResult("blocks", self.expStats.blocks)
        self.plotResult("deaths", self.expStats.deaths)
        self.plotResult("kills", self.expStats.kills)
        self.plotResult("doubles", self.expStats.doubles)
        self.plotResult("doubleDeaths", self.expStats.doubleDeaths)

    def plotResult(self, name, v):
        "Make a historgram plot of the given result"

        meanStr = "mean=%5.2f, std=%5.2f" % (np.mean(v), np.std(v))

        n, bins, patches = plt.hist(v, self.numBinsPlot, facecolor='blue', alpha=0.5)

        plt.xlabel(name)
        plt.ylabel("#")
        plt.title("%s from %d games (%s)" % (name, self.numGames, meanStr))
        
        if self.save:
            plt.savefig("%s_%s.png" % (self.expName, name))

        if self.verbosity > 0:
            plt.show()        

    def printStats(self, name, xs):
        "print the stats of the given data"
        print("%s mean=%5.2f std=%5.2f" % (name, np.mean(xs), np.std(xs)))

def main():
    # simple tests
    numGames = 100
    numPlayers = 4
    exp = Experiment('test', numGames, numPlayers, verbosity=1, save=False)
    exp.run()

if __name__ == "__main__":
    main()        
