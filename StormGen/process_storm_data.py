import csv
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

wind_max = []
pressure_min = []

with open('hurdat2-1851-2021-041922.txt', newline='') as f:
    reader = csv.reader(f)
    rows = list(reader)

    storm_count = 0
    r = 0

    while r < len(rows):
        rows_count = int(rows[r][2])
        storm_count += 1
        r += 1

        wind_speeds = [int(l[6]) for l in rows[r:r + rows_count]]

        wind_max.append(max(wind_speeds))

        pressures = [int(l[7]) for l in rows[r:r + rows_count] if int(l[7]) > 0]
        if pressures != []:
            pressure_min.append(min(pressures))
        else:
            pressure_min.append(-999)

        r += rows_count

plt.figure(0)
plt.hist([p for p in pressure_min if p > 0])

plt.figure(1)
plt.hist(wind_max, bins=range(min(wind_max), max(wind_max) + 5, 5))

plt.show()
