import os
import glob
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import gaussian_kde


def estimate_v_distr():
    path = os.path.join('input', 'CHAZ')
    points = []
    for file in glob.glob(os.path.join(path, "CHAZ*.csv")):
        df = pd.read_csv(file)
        points.extend(df["wspd"].values.tolist())

    ker = gaussian_kde(points)

    bounds = (min(points), max(points))

    # PLOT
    # eval_points = np.linspace(bounds[0], bounds[1], 1000)
    # prob = ker.pdf(eval_points)
    # plt.hist(points, bins=100, density=True)
    # plt.plot(eval_points, prob)

    # plt.savefig("Output/v_distr.png", transparent=True, bbox_inches='tight')

    # plt.show()

    return ker, bounds