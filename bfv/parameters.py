import math

class BFVParameters:
    def __init__(self, poly_degree: int, plain_modulus: int, ciph_modulus):
        self.poly_degree = poly_degree # d
        self.plain_modulus = plain_modulus # p
        self.ciph_modulus = ciph_modulus # q
        self.scaling_factor = ciph_modulus / plain_modulus # Δ = q/p
        
    def print_parameters(self):
        """Prints parameters.
        """
        print("Encryption parameters")
        print("\t polynomial degree: %d" %(self.poly_degree))
        print("\t plaintext modulus: %d" % (self.plain_modulus))
        print("\t ciphertext modulus size: %d bits" % (int(math.log(self.ciph_modulus, 2))))