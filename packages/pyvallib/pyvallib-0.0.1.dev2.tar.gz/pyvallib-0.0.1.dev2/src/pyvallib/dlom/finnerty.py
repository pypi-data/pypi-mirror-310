from statistics import NormalDist

import numpy as np


class Finnerty:
    """
    Calculates discount for lack of marketability based on the Finnerty
    Average-Strike Put Option Model
    """

    def __init__(self, T, sigma, q=0):
        self.T = T
        self.sigma = sigma
        self.q = q

    @property
    def s2_t(self):
        return self.sigma**2 * self.T

    @property
    def v_root_t(self):
        return np.sqrt(self.s2_t + np.log(2 * (np.exp(self.s2_t) - self.s2_t - 1)) - 2 * np.log(np.exp(self.s2_t) - 1))

    def calculate_dlom(self):
        """
        Calculate discount for lack of marketability
        """
        return np.exp(-self.q * self.T) * (NormalDist().cdf(self.v_root_t / 2) - NormalDist().cdf(-self.v_root_t / 2))

    def intermediate_calculations(self):
        """
        Calculate intermediate values for the model
        """
        return {"s2_t": self.s2_t, "v_root_t": self.v_root_t}

    citation = (
        "Finnerty, J.D. (1996) 'An Average-Strike Put Option Model of the Marketability Discount', "
        "The Journal of Derivatives, Summer 2012, 19(4) pp. 53-69."
    )
