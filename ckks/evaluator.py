from ckks.parameters import CKKSParameters
from util.crypto.ciphertext import Ciphertext
from util.crypto.plaintext import Plaintext
from util.crypto.public_key import PublicKey
from util.polynomial import Polynomial

class CKKSEvaluator:
    def __init__(self, params: CKKSParameters):
        self.poly_degree = params.poly_degree
        self.big_modulus = params.big_modulus
        self.scaling_factor = params.scaling_factor
        self.bootstrapping = None
        self.crt_context = params.crt_context
        
    def add(self, ct1: Ciphertext, ct2: Ciphertext) -> Ciphertext:
        assert ct1.modulus == ct2.modulus, "Ciphertext modulus are not same"
        assert ct1.scaling_factor == ct2.scaling_factor, "Ciphertext scaling factor are not same"
        modulus = ct1.modulus
        c0 = ct1.c0.add(ct2.c0, modulus).mod_small(modulus)
        c1 = ct1.c1.add(ct2.c1, modulus).mod_small(modulus)
        return Ciphertext(c0, c1, ct1.scaling_factor, modulus)
    
    def add_plain(self, ct: Ciphertext, pt: Plaintext) -> Ciphertext:
        assert ct.scaling_factor == pt.scaling_factor, "Ciphertext and Plaintext scaling factor are not same"
        modulus = ct.modulus
        c0 = ct.c0.add(pt.poly, modulus).mod_small(modulus)
        return Ciphertext(c0, ct.c1, ct.scaling_factor, modulus)
    
    def multiply(self, ct1: Ciphertext, ct2: Ciphertext, relin_key: PublicKey) -> Ciphertext:
        assert ct1.modulus == ct2.modulus, "Ciphertext modulus are not same"
        modulus = ct1.modulus
        
        # c0 = c0_1 * c0_2
        c0 = ct1.c0.multiply(ct2.c0, modulus, crt=self.crt_context).mod_small(modulus)
        # c1 = c0_1 * c1_2 + c1_1 * c0_2
        c1 = ct1.c0.multiply(ct2.c1, modulus, crt=self.crt_context) \
            .add(ct1.c1.multiply(ct2.c0, modulus, crt=self.crt_context), modulus) \
            .mod_small(modulus)
        # c2 = c1_1 * c1_2
        c2 = ct1.c1.multiply(ct2.c1, modulus, crt=self.crt_context).mod_small(modulus)
        
        return self.relinearize(
            relin_key, c0, c1, c2,
            new_scaling_factor=(ct1.scaling_factor * ct2.scaling_factor),
            modulus=modulus
        )
        
    def relinearize(self, relin_key: PublicKey, c0: Polynomial, c1: Polynomial, c2: Polynomial, new_scaling_factor: float, modulus: int) -> Ciphertext:
        # c0' = (p0 * c2)/big_modulus + c0
        new_c0 = relin_key.p0.multiply(c2, modulus * self.big_modulus, crt=self.crt_context) \
            .mod_small(modulus * self.big_modulus) \
            .divide(self.big_modulus) \
            .add(c0, modulus) \
            .mod_small(modulus)
        # c1' = (p1 * c2)/big_modulus + c1
        new_c1 = relin_key.p1.multiply(c2, modulus * self.big_modulus, crt=self.crt_context) \
            .mod_small(modulus * self.big_modulus) \
            .divide(self.big_modulus) \
            .add(c1, modulus) \
            .mod_small(modulus)
            
        return Ciphertext(new_c0, new_c1, new_scaling_factor, modulus)