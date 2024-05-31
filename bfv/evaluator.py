from bfv.relin_key import BFVRelinKey
from bfv.parameters import BFVParameters
from util.crypto.ciphertext import Ciphertext
from util.polynomial import Polynomial

class BFVEvaluator:
    def __init__(self, params: BFVParameters):
        self.plain_modulus = params.plain_modulus
        self.coeff_modulus = params.ciph_modulus
        self.scaling_factor = params.scaling_factor

    def add(self, a: Ciphertext, b: Ciphertext) -> Ciphertext:
        new_c0 = a.c0.add(b.c0, coeff_modulus=self.coeff_modulus)
        new_c1 = a.c1.add(b.c1, coeff_modulus=self.coeff_modulus)
        return Ciphertext(new_c0, new_c1)
    
    def multiply(self, a: Ciphertext, b: Ciphertext, relin_key: BFVRelinKey) -> Ciphertext:
        new_c0 = a.c0.fft_multiply(b.c0) \
            .scalar_multiply(1 / self.scaling_factor) \
            .round().mod(self.coeff_modulus)
        new_c1 = a.c0.fft_multiply(b.c1) \
            .add(a.c1.fft_multiply(b.c0)) \
            .scalar_multiply(1 / self.scaling_factor) \
            .round().mod(self.coeff_modulus)
        new_c2 = a.c1.fft_multiply(b.c1) \
            .scalar_multiply(1 / self.scaling_factor) \
            .round().mod(self.coeff_modulus)
        
        return self.relinealize(relin_key, new_c0, new_c1, new_c2)
    
    def relinealize(self, relin_key: BFVRelinKey, c0: Polynomial, c1: Polynomial, c2: Polynomial) -> Ciphertext:
        (keys, base) = (relin_key.keys, relin_key.base)
        num_levels = len(keys)

        c2_decomposed = c2.base_decompose(base, num_levels)
        new_c0 = c0
        new_c1 = c1

        for i in range(num_levels):
            new_c0 = new_c0.add(keys[i][0].multiply(c2_decomposed[i], self.coeff_modulus), self.coeff_modulus)
            new_c1 = new_c1.add(keys[i][1].multiply(c2_decomposed[i], self.coeff_modulus), self.coeff_modulus)

        return Ciphertext(new_c0, new_c1)

