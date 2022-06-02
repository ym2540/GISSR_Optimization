import pandas as pd

from sklearn.gaussian_process.kernels import RBF
from sklearn.gaussian_process import GaussianProcessRegressor


def generate_GP_SR(file=r"Output/sr_ideal_opt_grid_search_all_ens.csv", kernel=RBF(), alpha=1, normalize_y=True, optimizer=None, random_state=None):

    points = pd.read_csv(file, usecols=["x", "d"]).to_numpy()
    x = points[:, 0]
    d = points[:, 1]

    gpr = GaussianProcessRegressor(kernel=kernel, alpha=alpha, random_state=random_state, normalize_y=normalize_y, optimizer=optimizer)
    gpr.fit(x.reshape(-1, 1), d.reshape(-1, 1))

    return gpr


def generate_GP_GC():
    pass
