class Optimizer:

    def __init__(self, Acq, Model):
        self.Acq = Acq
        self.Model = Model

    def optimize(self):
        converged = False
        while not converged:
            job_id = 0
            next_point = self.Acq_func.get_next_point()
            
            # Run GeoClaw on next_point (calculate all GC params from next_point) (Either: Acq func has convergence criteria or max computation time)
            # Extract time series for all inside gauges with some resolution (HYP: resolution) 
            # Superimpose tide at all time steps and all gauges (distances)
            # Perturb tide stage and superimpose to get points around tide stage (HYP: max perturb, perturb resolution, added error?)
            # Get surge_peak and damage for all points
            # Extract time series for all outside gauges with SR resolution
            # Superimpose tide and perturbed tides on SR time series
            # Run SR on same points for reference? (Measures error against ground truth, and error aginst perturbed solutions), maybe correct for error?
            # Perturb x on all SR points. Run SR. (HYP: max perturb, resolution)
            # Should have new points: GC_true for all gauges, GC_perturbed_tide for all gauges, SR_perturbed_x for all GC_perturbed and GC_true
            # Added error to SR?
            # Add points, refit GP_GC

        # Marginalize GP_GC, simple minimization!
