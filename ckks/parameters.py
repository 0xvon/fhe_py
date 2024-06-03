import math

from util.math.crt import CRTContext

class CKKSParameters:
    def __init__(self, poly_degree: int, ciph_modulus: int, big_modulus: int, scaling_factor: float, taylor_iterations=6, prime_size=59):
        self.poly_degree = poly_degree # d
        self.ciph_modulus = ciph_modulus # p
        self.big_modulus = big_modulus # q: large modulus used for bootstrapping
        self.scaling_factor = scaling_factor # scaling factor to multiply by.
        self.num_taylor_iterations = taylor_iterations # number of iterations to perform for Taylor series in bootstrapping
        self.hamming_weight = poly_degree // 4
        self.crt_context = None
        
        if prime_size:
            # 1 + log2(d) + 4 * log2(q) / s
            num_primes = 1 + int((1 + math.log(poly_degree, 2) + 4 * math.log(big_modulus, 2) \
                / prime_size))
            self.crt_context = CRTContext(num_primes, prime_size, poly_degree)
            
    def print_parameters(self):
        """Prints parameters.
        """
        print("Encryption parameters")
        print("\t Polynomial degree: %d" %(self.poly_degree))
        print("\t Ciphertext modulus size: %d bits" % (int(math.log(self.ciph_modulus, 2))))
        print("\t Big ciphertext modulus size: %d bits" % (int(math.log(self.big_modulus, 2))))
        print("\t Scaling factor size: %d bits" % (int(math.log(self.scaling_factor, 2))))
        print("\t Number of Taylor iterations: %d" % (self.num_taylor_iterations))
        if self.crt_context:
            rns = "Yes"
        else:
            rns = "No"
        print("\t RNS: %s" % (rns))