from typing import Optional
from ckks.parameters import CKKSParameters
from util.crypto.ciphertext import Ciphertext
from util.crypto.plaintext import Plaintext
from util.crypto.secret_key import SecretKey
from util.polynomial import Polynomial

class CKKSDecryptor:
    def __init__(self, params: CKKSParameters, secret_key: SecretKey):
        self.poly_degree = params.poly_degree
        self.crt_context = params.crt_context
        self.secret_key = secret_key
        
    def decrypt(self, ciphertext: Ciphertext, c2: Optional[Polynomial] = None):
        assert ciphertext.modulus is not None, "Ciphertext modulus is not provided"
        assert ciphertext.scaling_factor is not None, "Ciphertext scaling factor is not provided"
        
        (c0, c1) = (ciphertext.c0, ciphertext.c1)
        
        # m = c1 * s + c0
        m = c1.multiply(self.secret_key.s, ciphertext.modulus, crt=self.crt_context) \
            .add(c0, ciphertext.modulus)
            
        if c2:
            sk_squared = self.secret_key.s.multiply(self.secret_key.s, ciphertext.modulus)
            c2_m = c2.multiply(sk_squared, ciphertext.modulus, crt=self.crt_context)
            m = m.add(c2_m, ciphertext.modulus)
            
        m = m.mod_small(ciphertext.modulus)
        return Plaintext(m, ciphertext.scaling_factor)