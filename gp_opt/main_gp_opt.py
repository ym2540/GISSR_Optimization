from scipy.stats import uniform

import Acquisition
import Optimizer

from fun_opt import generate_GP_SR, generate_GP_GC
from estimate_tide_distr import estimate_tide_distr
from Model import Model
from Tide_class import Tide


"""
FULL FLOW SHOULD BE:
1. Generate initial GP for SR (HYP: Kernel, (Mean func), Kernel HYP)
2. Generate initial GP for GC (HYP: Kernels for all dims, Kernel HYP)
3. Set parameter (x and storm phi) priors (Distributions and boundaries)
4. Create Model class with above
5. Create acquisition function for x with model
6. Create acquisition function for phi with model
7. Create Optimizer class with acquisition functions and model
8. Optimize
"""


GP_GC = generate_GP_GC()  # TODO write func and calibrate hyperparams
GP_SR = generate_GP_SR()  # TODO calibrate hyperparams

Tide = Tide()
tide_ker, tide_bounds = estimate_tide_distr(Tide)


X = uniform(a=1.9, b=6)  # uniform prior on X (wall height), lb=1.9 m (lowest shore height), ub=6m (arbitrary, from previous test runs)
X_bounds = (1.9, 6)

variables = {'zeta': {'pdf': tide_ker.pdf, 'bounds': tide_bounds, 'initial': 0}, 'x': {'pdf': X.pdf, 'bounds': X_bounds, 'initial': 2}}  # TODO add other vars
phi_keys = ['zeta']  # list of phi keys in variables

M = Model(GP_SR, GP_GC, variables, phi_keys)

beta_x = Acquisition.Beta_const(0.3)  # TODO Determine value and func
beta_phi = Acquisition.Beta_const(0.4)  # TODO Determine value and func

Acq_x = Acquisition.Acq_x_UCB(beta_x, M)
Acq_phi = Acquisition.Acq_phi_EUCB(beta_phi, M)
A = Acquisition.Acquisition(Acq_x, Acq_phi)

Opt = Optimizer.Optimizer(A, M)
x = Opt.optimize() # TODO
