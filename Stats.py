import numpy as np

class Stats:

    """
    A simple class for storing some results
    we'll want to gather statistics on
    """

    def __init__(self, size):

        self.winTurns = np.zeros(size)
        self.turns = np.zeros(size)
        self.blocks = np.zeros(size)
        self.kills = np.zeros(size)
        self.deaths = np.zeros(size)
        self.doubles = np.zeros(size)
        self.doubleDeaths = np.zeros(size)

