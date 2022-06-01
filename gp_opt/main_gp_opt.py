import estimate_tide_distr
from Tide_class import Tide

"""
FULL FLOW SHOULD BE:
0. Init GeoClaw with correct topo
1. Generate initial GP for SR (HYP: Kernel, (Mean func), Kernel HYP)
2. Generate initial GP for GC (HYP: Kernels for all dims, Kernel HYP)
3. Set parameter (x and storm phi) priors (Distributions and boundaries)
4. Create Model class with above
5. Create acquisition function for x with model
6. Create acquisition function for phi with model
7. Create Optimizer class with acquisition functions and model
8. Optimize
"""

Tide = Tide()
tide_ker = estimate_tide_distr(Tide)