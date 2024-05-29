from typing import Optional
from util.polynomial import Polynomial

class Plaintext:
    def __init__(self, poly: Polynomial, scaling_factor: Optional[float] = None):
        """Initializes a plaintext object with a polynomial and scaling factor.
        poly: Plaintext Polynomial
        scaling_factor: Scaling factor for the plaintext polynomial
        """
        self.poly = poly
        self.scaling_factor = scaling_factor
        
    def __str__(self):
        return str(self.poly)