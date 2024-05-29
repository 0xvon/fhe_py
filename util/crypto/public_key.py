from util.polynomial import Polynomial

class PublicKey:
    def __init__(self, p0: Polynomial, p1: Polynomial):
        """Initializes a public key object with two polynomials.
        p0: First element polynomial
        p1: Second element polynomial
        """
        self.p0 = p0
        self.p1 = p1
        
    def __str__(self):
        return 'P0: %s\nP1: %s' %(str(self.p0), str(self.p1))