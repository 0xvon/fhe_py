from bfv.parameters import BFVParameters
from util.crypto.ciphertext import Ciphertext
from util.crypto.plaintext import Plaintext
from util.crypto.public_key import PublicKey
from util.polynomial import Polynomial
from util.random_sampling import sample_triangle

class BFVEncryptor:
    def __init__(self, params: BFVParameters, public_key: PublicKey):
        self.poly_degree = params.poly_degree
        self.coeff_modulus = params.ciph_modulus
        self.public_key = public_key
        self.scaling_factor = int(params.scaling_factor)        
        
    def encrypt(self, message: Plaintext) -> Ciphertext:
        p0 = self.public_key.p0
        p1 = self.public_key.p1
        scaled_message = message.poly.scalar_multiply(self.scaling_factor, self.coeff_modulus)
        random_vec = Polynomial(self.poly_degree, sample_triangle(self.poly_degree))
        error1 = Polynomial(self.poly_degree, sample_triangle(self.poly_degree))
        error1 = Polynomial(self.poly_degree, [0] * self.poly_degree)
        error2 = Polynomial(self.poly_degree, sample_triangle(self.poly_degree))
        error2 = Polynomial(self.poly_degree, [0] * self.poly_degree)
        c0 = error1 \
            .add(p0.multiply(random_vec, self.coeff_modulus), self.coeff_modulus) \
            .add(scaled_message, self.coeff_modulus)
        c1 = error2.add(p1.multiply(random_vec, self.coeff_modulus), self.coeff_modulus)
        
        return Ciphertext(c0, c1)
            