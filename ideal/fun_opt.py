import pandas as pd

from sklearn.gaussian_process.kernels import RBF
from sklearn.gaussian_process import GaussianProcessRegressor
from scipy.optimize import minimize_scalar



"""
FULL FLOW SHOULD BE:
1. Generate initial GP for SR
2. Generate initial GP for GC
3. Set parameter (x and storm phi) priors
4. Create Model class with above
5. Create acquisition function for x with model
6. Create acquisition function for phi with model
7. Create Optimizer class with acquisition functions and model
8. Optimize
"""


class Optimizer:

    def __init__(self, Acq, Model):
        self.Acq = Acq
        self.Model = Model

    def optimize(self):
        next_point = self.Acq_func.get_next_point()
        # Run GeoClaw on next_point
        # Extract time series for all inside gauges with some resolution (HYP: resolution)
        # Superimpose tide at all time steps and all gauges (distances)
        # Perturb tide stage and superimpose to get points around tide stage (HYP: distance, added error?)
        # SR


class Model:
    """

    """

    def __init__(self, SR_GP, GC_GP, params):

        self.SR_GP = SR_GP
        self.GC_GP = GC_GP
        self.params = params

    def marginalize_GC_GP(self):
        """
        Marginalizes out all storm parameters from GP. Integrates p(phi)*d(x | phi) d phi
        """
        self.GC_GP_marg
        pass

    def query_fused(self, points, method="avg", return_std=False):
        """

        """
        points = points.reshape(-1,1)
        if method == "avg":
            m_SR, std_SR = self.SR_GP.predict(points, return_std=True)
            m_GC, std_GC = self.GC_GP_marg.predict(points, return_std=True)
            a = std_SR / (std_SR + std_GC)

            m_fused = a * m_GC + (1 - a) * m_SR
            std_fused = (a ** 2) * std_GC ** 2 + ((1 - a) ** 2) * std_SR ** 2

            if return_std:
                return m_fused, std_fused
            return m_fused


class Acquisition:
    def __init__(self, Acq_x, Acq_phi):
        self.Acq_x = Acq_x
        self.Acq_phi = Acq_phi

    def next_point(self):
        x = self.Acq_x.get_next_point()
        phi = self.Acq_phi.get_next_point()
        return x, phi


class UCB:
    """
    GP Upper Confidence Bound Acq func. ONLY for x values (due to query_fused func hardcoding)

    """
    def __init__(self, beta, Model):
        self.beta = beta
        self.Model = Model

    def objective(self, Model, x):
        m, std = self.Model.query_fused(x)
        return m - self.beta * std

    def get_next_point(self):
        f = lambda x: self.objective(self.Model, x)
        next_point = minimize_scalar(f, method='brent', bounds=Model.params["x"].bounds)
        return next_point


class SOME_ACQ_FUNC_FOR_PHI:
    """
    Should combine minimization of uncertainty (std of phi) at high p(phi) and high d(x, phi) spots  
    """
    def __init__(self, Model):
        self.Model = Model

    def get_next_point(self):
        pass


def generate_SR_GP(file=r"Output/sr_ideal_opt_grid_search_all_ens.csv", kernel=RBF(), alpha=1, normalize_y=True, optimizer=None, random_state=None):

    points = pd.read_csv(file, usecols=["x", "d"]).to_numpy()
    x = points[:,0]
    d = points[:,1]

    gpr = GaussianProcessRegressor(kernel=kernel, alpha=alpha, random_state=random_state, normalize_y=normalize_y, optimizer=optimizer)
    gpr.fit(x.reshape(-1,1), d.reshape(-1,1))

    return gpr