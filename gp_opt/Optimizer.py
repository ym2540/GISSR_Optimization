import makerun

class Optimizer:

    def __init__(self, Acq, Model):
        self.Acq = Acq
        self.Model = Model

    def optimize(self):
        converged = False
        while not converged:
            job_id = 0
            x_next, phi_next = self.Acq.get_next_point()

            makerun.make_all(job_id, x_next, phi_next)
            Job = makerun.GC_job(job_id, x_next, phi_next)
            Job.run()
            # Extract time series from outside gauges for SR (res)
            # Superimpose tide at all time steps and all gauges (distances), both inside and outside
            # Perturb tide stage and superimpose to get points around tide stage (HYP: max perturb, perturb resolution, added error?)
            # Get surge_peak for all points. Calculate volume through simple topo. Recalculate height from surfaceV func. Get damage (use N)
            # 
            # Run SR on same points for reference? (Measures error against ground truth, and error aginst perturbed solutions), maybe correct for error?
            # Perturb x on all SR points. Run SR. (HYP: max perturb, resolution)
            # Should have new points: GC_true for all gauges, GC_perturbed_tide for all gauges, SR_perturbed_x for all GC_perturbed and GC_true
            # Added error to SR?
            # Add points, refit GP_GC

        # Marginalize GP_GC, simple minimization!
