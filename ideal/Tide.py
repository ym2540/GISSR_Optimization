import pandas as pd
import numpy as np

class Tide:
    def __init__(self, const_file="Input/tidal_constituents.csv"):
        constituents = pd.read_csv(const_file)
        self.amplitudes =  constituents["Amplitude"].to_numpy()
        self.phases = constituents["Phase"].to_numpy()
        self.speeds = constituents["Speed"].to_numpy()

    def get_tide_height(self, t):
        return np.sum(self.amplitudes * np.cos(t * self.speeds + self.phases))