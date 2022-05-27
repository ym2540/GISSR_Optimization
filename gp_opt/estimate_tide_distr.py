from Tide import Tide
from matplotlib import pyplot
import numpy as np

N = 1000000
timescale=80*365.25*24
ts = np.linspace(0,timescale, N)

Tide = Tide()

points = [None]*N
i = 0
for t in ts:
    h = Tide.get_tide_height(t)
    points[i] = h
    i += 1

pyplot.hist(points, bins=1000)
pyplot.show()
