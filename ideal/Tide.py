import pandas as pd
import numpy as np
import random as rnd

class Tide:
    def __init__(self, const_file="Input/tidal_constituents.csv"):
        constituents = pd.read_csv(const_file)
        self.amplitudes =  constituents["Amplitude"].to_numpy()
        self.phases = constituents["Phase"].to_numpy()
        self.speeds = constituents["Speed"].to_numpy()

    def get_tide_height(self, t):
        return np.sum(self.amplitudes * np.cos(t * self.speeds + self.phases))

    def get_random_tide_height(self, timescale=80*365.25*24):
        t = rnd.uniform(0, timescale)
        return self.get_tide_height(t)

    def superimpose_tide_height(self, t_peak,):
        pass