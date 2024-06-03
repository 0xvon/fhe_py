from typing import Optional
from ckks.parameters import CKKSParameters
from util.crypto.ciphertext import Ciphertext
from util.crypto.plaintext import Plaintext
from util.crypto.public_key import PublicKey
from util.crypto.secret_key import SecretKey
from util.polynomial import Polynomial
from util.random_sampling import sample_triangle

class CKKSEncryptor:
    def __init__(self, params: CKKSParameters, public_key: PublicKey, secret_key: Optional[SecretKey] = None):
        self.poly_degree = params.poly_degree
        self.coeff_modulus = params.ciph_modulus
        self.big_modulus = params.big_modulus
        self.crt_context = params.crt_context
        self.public_key = public_key
        self.secret_key = secret_key
        
    def encrypt_with_sk(self, plaintext: Plaintext) -> Ciphertext:
        assert self.secret_key is not None, "Secret key is not provided"
        
        sk = self.secret_key.s
        r = Polynomial(self.poly_degree, sample_triangle(self.poly_degree))
        e = Polynomial(self.poly_degree, sample_triangle(self.poly_degree))
        # c0 = s*r + e + m
        c0 = sk.multiply(r, self.coeff_modulus, crt=self.crt_context) \
            .add(e, self.coeff_modulus) \
            .add(plaintext.poly, self.coeff_modulus) \
            .mod_small(self.coeff_modulus)
        # c1 = -r
        c1 = r.scalar_multiply(-1, self.coeff_modulus).mod_small(self.coeff_modulus)
        return Ciphertext(c0, c1, plaintext.scaling_factor, self.coeff_modulus)
    
    def encrypt(self, plaintext: Plaintext) -> Ciphertext:
        p0 = self.public_key.p0
        p1 = self.public_key.p1
        
        r = Polynomial(self.poly_degree, sample_triangle(self.poly_degree))
        e1 = Polynomial(self.poly_degree, sample_triangle(self.poly_degree))
        e2 = Polynomial(self.poly_degree, sample_triangle(self.poly_degree))
        # c0 = p0 * r + e1 + m
        c0 = p0.multiply(r, self.coeff_modulus, crt=self.crt_context) \
            .add(e1, self.coeff_modulus) \
            .add(plaintext.poly, self.coeff_modulus) \
            .mod_small(self.coeff_modulus)
        # c1 = p1 * r + e2
        c1 = p1.multiply(r, self.coeff_modulus, crt=self.crt_context) \
            .add(e2, self.coeff_modulus) \
            .mod_small(self.coeff_modulus)
            
        return Ciphertext(c0, c1, plaintext.scaling_factor, self.coeff_modulus)
    
    def raise_modulus(self, new_modulus: int):
        """Rescales scheme to have a new modulus.
        Raises ciphertext modulus.
        """
        self.coeff_modulus = new_modulus