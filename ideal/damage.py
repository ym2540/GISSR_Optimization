import pandas as pd
import numpy as np
from math import floor


class Damage:
    def __init__(self, damage_table):
        self.damage_table = pd.read_csv(damage_table)
        self.water_level = self.damage_table["water_level"]
        self.h_min = self.damage_table["water_level"].values[0]
        self.h_max = self.damage_table["water_level"].values[-1]
        self.step = self.damage_table["water_level"].size

    def calc_damage(self, water_level):
        damage = np.zeros(water_level.shape)
        for div in range(water_level.shape[1]):
            for s, storm in enumerate(water_level[:, div]):
                index = floor((water_level[s, div] - self.h_min) / self.step)

                damage[s, div] = self.damage_table[str(div)][index] + (water_level[s, div] - self.water_level[index])*(self.damage_table[str(div)][index + 1] - self.damage_table[str(div)][index])
        return damage
