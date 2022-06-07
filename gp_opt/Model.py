
class Model:
    """
    
    """

    def __init__(self, GP_SR, GP_GC, params, phi_keys):
        """
        Input:
            GP_SR:
            GP_GC: 
            params: A dict of params to dicts which contains 'bounds' touple(min, max) (bounds on parameter), 'pdf' function (probability density function), 'initial' float (some initial point, eg. prior on x from GP_SR or highest prop for phi)
            phi_keys: List of keys (str) for all phi parameters, eg: 'wind_speed'
        """

        self.GP_SR = GP_SR
        self.GP_GC = GP_GC
        self.params = params
        self.phi_keys = phi_keys

    def marginalize_GP_GC(self):
        """
        Marginalizes out all storm parameters from GP. Integrates p(phi)*d(x | phi) d phi TODO
        """
        self.GP_GC_marg
        pass

    def query_fused(self, points, method='avg', return_std=False):
        """

        """
        points = points.reshape(-1,1)
        if method == "avg":
            m_SR, std_SR = self.GP_SR.predict(points, return_std=return_std)
            m_GC, std_GC = self.GP_GC_marg.predict(points, return_std=return_std)
            a = std_SR / (std_SR + std_GC)

            m_fused = a * m_GC + (1 - a) * m_SR
            std_fused = (a ** 2) * std_GC ** 2 + ((1 - a) ** 2) * std_SR ** 2

            if return_std:
                return m_fused, std_fused
            return m_fused

    def query_GP_GC(self, points, return_std=False):
        """
        Input:
            points: array of shape (n_samples, n_features) or list of objects
        """
        m_GC, std_GC = self.GP_GC.predict.predict(points, return_std=return_std)
        return m_GC, std_GC