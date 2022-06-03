import os
import glob
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import gaussian_kde


def estimate_alpha_distr():
    path = os.path.join('input', 'CHAZ')
    points = []
    for file in glob.glob(os.path.join(path, "CHAZ*.csv")):
        df = pd.read_csv(file)
        points.extend(df["trdir"].dropna().values.tolist())

    ker = gaussian_kde(points)

    bounds = (min(points), max(points))

    # PLOT
    eval_points = np.linspace(bounds[0], bounds[1], 1000)
    prob = ker.pdf(eval_points)
    plt.hist(points, bins=8, density=True)
    plt.plot(eval_points, prob)
    plt.xlabel(r'Heading (degrees)')
    plt.ylabel('Probability')

    #plt.savefig("Output/heading_distr.png", transparent=True, bbox_inches='tight')

    plt.show()

    return ker, bounds


estimate_alpha_distr()
