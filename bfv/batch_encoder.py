from typing import List
from util.crypto.plaintext import Plaintext
from util.math.ntt import NTTContext
from util.polynomial import Polynomial

class BatchEncoder:
    def __init__(self, params):
        self.degree = params.poly_degree
        self.plain_modulus = params.plain_modulus
        self.ntt = NTTContext(params.poly_degree, params.plain_modulus)
        
    def encode(self, values: List[int]) -> Plaintext:
        assert len(values) == self.degree, 'Invalid number of values'
        coeffs = self.ntt.ftt_inv(values)
        return Plaintext(Polynomial(self.degree, coeffs))
    
    def decode(self, plain: Plaintext) -> List[int]:
        result = self.ntt.ftt_fwd(plain.poly.coeffs)
        return [val % self.plain_modulus for val in result]