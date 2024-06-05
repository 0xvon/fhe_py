from typing import List
from ckks.parameters import CKKSParameters
from util.crypto.plaintext import Plaintext
from util.math.ntt import FFTContext
from util.polynomial import Polynomial

class CKKSEncoder:
    def __init__(self, params: CKKSParameters):
        self.degree = params.poly_degree
        self.fft = FFTContext(self.degree * 2)
        
    def encode(self, values: List[float], scaling_factor: float) -> Plaintext:
        num_values = len(values)
        plain_len = num_values << 1
        # Canonical embedding inverse variant.
        to_scale = self.fft.embedding_inv(values)
        
        m = [0] * plain_len
        for i in range(num_values):
            m[i] = int(to_scale[i].real * scaling_factor + 0.5)
            m[i + num_values] = int(to_scale[i].imag * scaling_factor + 0.5)
            
        return Plaintext(Polynomial(plain_len, m), scaling_factor)
    
    def decode(self, plain: Plaintext) -> List[float]:
        plain_len = len(plain.poly.coeffs)
        num_values = plain_len >> 1
        
        m = [0] * num_values
        for i in range(num_values):
            m[i] = complex(
                plain.poly.coeffs[i] / plain.scaling_factor,
                plain.poly.coeffs[i + num_values] / plain.scaling_factor
            )
            
        return self.fft.embedding(m)
        
        