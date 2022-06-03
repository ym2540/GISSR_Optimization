from matplotlib import pyplot as plt
from scipy.stats import gaussian_kde
from Tide_class import Tide
import numpy as np


def estimate_tide_distr(Tide):
    N = 1000000
    timescale = 80 * 365.25 * 24
    ts = np.linspace(0, timescale, N)
    
    points = [None] * N
    i = 0
    for t in ts:
        h = Tide.get_tide_height(t)
        points[i] = h
        i += 1

    ker = gaussian_kde(points)

    bounds = (np.min(points), np.max(points))
    # PLOT
    # h_min = min(points)
    # h_max = max(points)
    # eval_points = np.linspace(h_min, h_max, 1000)
    
    # y = ker.pdf(eval_points)
    # plt.hist(points, bins=100, density=True)
    # plt.plot(eval_points, y)

    # plt.xlabel(r'Tide height (m) above MSL')
    # plt.ylabel(r'Probability')
    # #plt.show()

    # plt.savefig("Output/tide_distr.png", transparent=True, bbox_inches='tight')

    return ker, bounds
