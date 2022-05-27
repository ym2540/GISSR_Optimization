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


class UCB:
    """
    GP Upper Confidence Bound Acq func. ONLY for x values (due to query_fused func hardcoding)

    """
    def __init__(self, beta, Model):
        self.beta = beta
        self.Model = Model

    def objective(self, x):
        m, std = self.Model.query_fused(x, return_std=True)
        return m - self.beta * std

    def get_next_point(self):
        f = lambda x: self.objective(x)
        res = minimize_scalar(f, method='brent', bounds=self.Model.params["x"].bounds)
        
        if not res.success:
            raise Exception(res.message)
        return res.x


class SOME_ACQ_FUNC_FOR_PHI:
    """
    Should combine minimization of uncertainty (std of phi) at high p(phi) and high d(x, phi) spots
    """
    def __init__(self, beta, Model):
        self.Model = Model
        self.beta = beta

    def objective(self, phi, x):
        point = np.insert(phi, 0, x)
        m, std = self.Model.query_GP_GC(point)
        p_phi = 1
        for val, param in enumerate(self.Model.phi_keys):
            p_phi = p_phi * self.Model.params[param]["pdf"](val)  # TODO
        return p_phi * (m + self.beta * std)

    def get_next_point(self, x):
        f = lambda phi: - self.objective(phi, x)
        phi0 = np.array([p0["initial"] for p0 in itemgetter(self.Model.phi_keys)(self.Model.params)])
        bounds = [param["bounds"] for param in itemgetter(self.Model.phi_keys)(self.Model.params)]
        res = minimize(f, phi0, args=x, method='Nelder-Mead', bounds=bounds)

        if not res.success:
            raise Exception(res.message)
        return res.x