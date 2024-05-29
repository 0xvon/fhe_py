from typing import Optional
from util.polynomial import Polynomial

class Ciphertext:
    def __init__(self, c0: Polynomial, c1: Polynomial, scaling_factor: Optional[float] = None, modulus: Optional[int] = None):
        """Initializes a ciphertext object with two polynomials and scaling factor.
        c0: First element polynomial
        c1: Second element polynomial
        scaling_factor: Scaling factor for the ciphertext polynomial
        """
        self.c0 = c0
        self.c1 = c1
        self.scaling_factor = scaling_factor
        self.modulus = modulus
        
    def __str__(self):
        return 'C0: %s\nC1: %s' %(str(self.c0), str(self.c1))