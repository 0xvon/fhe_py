from ckks.parameters import CKKSParameters
from util.crypto.public_key import PublicKey
from util.crypto.rotation_key import RotationKey
from util.crypto.secret_key import SecretKey
from util.polynomial import Polynomial
from util.random_sampling import sample_hamming_weight_vector, sample_triangle, sample_uniform

class CKKSKeyGenerator:
    def __init__(self, params: CKKSParameters):
        self.params = params
        self.generate_secret_key(params)
        self.generate_public_key(params)
        self.generate_relin_key(params)
        
    def generate_secret_key(self, params: CKKSParameters):
        """Generates CKKS Secret key.
        s = (s_0, s_1, ..., s_n-1) where s_i ~ U(0, 1)
        """
        key = sample_hamming_weight_vector(params.poly_degree, params.hamming_weight)
        self.secret_key = SecretKey(Polynomial(params.poly_degree, key))
        
    def generate_public_key(self, params: CKKSParameters):
        mod = self.params.big_modulus
        pk_coeff = Polynomial(params.poly_degree, sample_uniform(0, mod, params.poly_degree))
        pk_error = Polynomial(params.poly_degree, sample_triangle(params.poly_degree))
        # p0 = -a * s + e
        p0 = pk_coeff.multiply(self.secret_key.s, mod) \
            .scalar_multiply(-1, mod) \
            .add(pk_error, mod)
        # p1 = a
        p1 = pk_coeff
        self.public_key = PublicKey(p0, p1)
        
    def generate_switching_key(self, new_key: Polynomial):
        mod = self.params.big_modulus
        mod_squared = mod ** 2
        
        # coeff = chosed randomly from U(0, mod^2)
        swk_coeff = Polynomial(self.params.poly_degree, sample_uniform(0, mod_squared, self.params.poly_degree))
        swk_error = Polynomial(self.params.poly_degree, sample_triangle(self.params.poly_degree))
        
        # (-coeff * s) + e + (new_key * mod)
        sw0 = swk_coeff.multiply(self.secret_key.s, mod_squared) \
            .scalar_multiply(-1, mod_squared) \
            .add(swk_error, mod_squared) \
            .add(new_key.scalar_multiply(mod, mod_squared), mod_squared)
        sw1 = swk_coeff
        return PublicKey(sw0, sw1)
        
    def generate_relin_key(self, params: CKKSParameters):
        # s^2 % big_modulus
        sk_squared = self.secret_key.s.multiply(self.secret_key.s, params.big_modulus)
        self.relin_key = self.generate_switching_key(sk_squared)
        
    def generate_rot_key(self, rotation: int):
        # rotate its coeffs by rotation
        new_key = self.secret_key.s.rotate(rotation)
        rk = self.generate_switching_key(new_key)
        return RotationKey(rotation, rk)
        
    def generate_conj_key(self):
        # Generate K_{-1}(s).
        new_key = self.secret_key.s.conjugate()
        return self.generate_switching_key(new_key)
    