from typing import Optional

from sympy import Q
from bfv.parameters import BFVParameters
from util.crypto.ciphertext import Ciphertext
from util.crypto.plaintext import Plaintext
from util.crypto.secret_key import SecretKey
from util.polynomial import Polynomial


class BFVDecryptor:
    def __init__(self, params: BFVParameters, secret_key: SecretKey):
        self.poly_degree = params.poly_degree
        self.ciph_modulus = params.ciph_modulus
        self.plain_modulus = params.plain_modulus
        self.scaling_factor = params.scaling_factor
        self.secret_key = secret_key

    def decrypt(self, ciphertext: Ciphertext, c2: Optional[Polynomial] = None) -> Plaintext:
        (c0, c1) = (ciphertext.c0, ciphertext.c1)
        intermed_message = c0.add(c1.multiply(self.secret_key.s, self.ciph_modulus), self.ciph_modulus)
        if c2:
            secret_key_squared = self.secret_key.s.multiply(self.secret_key.s, self.ciph_modulus)        
            intermed_message = intermed_message.add(c2.multiply(secret_key_squared, self.ciph_modulus), self.ciph_modulus)            
        
        intermed_message = intermed_message.scalar_multiply(1 / self.scaling_factor)
        intermed_message = intermed_message.round()
        intermed_message = intermed_message.mod(self.plain_modulus)
        return Plaintext(intermed_message)