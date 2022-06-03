import numpy as np

from scipy.optimize import minimize_scalar, minimize
from operator import itemgetter


class Acquisition:
    """
    General acquisition class for storing x and phi acquisition functions
    """
    def __init__(self, Acq_x, Acq_phi):
        self.Acq_x = Acq_x
        self.Acq_phi = Acq_phi

    def next_point(self):
        x = self.Acq_x.get_next_point()
        phi = self.Acq_phi.get_next_point()
        return x, phi


class Acq_x_UCB:
    """
    GP Upper Confidence Bound Acq func. ONLY for x values (due to query_fused func hardcoding)

    """
    def __init__(self, beta_func, Model):
        self.beta_func = beta_func
        self.Model = Model

    def objective(self, x, beta):
        m, std = self.Model.query_fused(x, return_std=True)
        return m - beta * std

    def get_next_point(self, beta=None):
        if beta is None:
            beta = self.beta_func()
        f = lambda x: self.objective(x, beta)
        res = minimize_scalar(f, method='brent', bounds=self.Model.params["x"].bounds)

        if not res.success:
            raise Exception(res.message)
        return res.x


class Acq_phi_EUCB:
    """
    Selects next storm param based on combination of probability of phi, mean of phi, and std of phi. 
    """
    def __init__(self, beta_func, Model):
        self.Model = Model
        self.beta_func = beta_func

    def objective(self, phi, x, beta):
        point = np.insert(phi, 0, x)
        m, std = self.Model.query_GP_GC(point)
        p_phi = 1
        for val, param in enumerate(self.Model.phi_keys):
            p_phi = p_phi * self.Model.params[param]["pdf"](val)  # TODO
        return p_phi * (m + beta * std)

    def get_next_point(self, x, beta=None):
        if beta is None:
            beta = self.beta_func()
        f = lambda phi: - self.objective(phi, x, beta)
        phi0 = np.array([p0["initial"] for p0 in itemgetter(self.Model.phi_keys)(self.Model.params)])
        bounds = [param["bounds"] for param in itemgetter(self.Model.phi_keys)(self.Model.params)]
        res = minimize(f, phi0, args=x, method='Nelder-Mead', bounds=bounds)

        if not res.success:
            raise Exception(res.message)
        return res.x


class Beta_const:

    def __init__(self, beta):
        self.beta = beta

    def get(self):
        return self.beta
