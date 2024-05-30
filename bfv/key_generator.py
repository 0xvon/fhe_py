from math import ceil, floor, log, sqrt
from bfv.parameters import BFVParameters
from bfv.relin_key import BFVRelinKey
from util.crypto.public_key import PublicKey
from util.crypto.secret_key import SecretKey
from util.polynomial import Polynomial
from util.random_sampling import sample_triangle, sample_uniform

class BFVKeyGenerator:
    def __init__(self, params: BFVParameters):
        self.generate_secret_key(params)
        self.generate_public_key(params)
        
    def generate_secret_key(self, params: BFVParameters):
        self.secret_key = SecretKey(Polynomial(params.poly_degree, sample_triangle(params.poly_degree)))
        
    def generate_public_key(self, params: BFVParameters):
        pk_coeff = Polynomial(params.poly_degree, sample_uniform(0, params.ciph_modulus, params.poly_degree))
        pk_error = Polynomial(params.poly_degree, sample_triangle(params.poly_degree))
        
        p0 = pk_error.add(
            pk_coeff.multiply(
                self.secret_key.s,
                params.ciph_modulus
            ),
            params.ciph_modulus
        ).scalar_multiply(-1, params.ciph_modulus)
        p1 = pk_coeff
        self.public_key = PublicKey(p0, p1)
        
    def generate_relin_key(self, params: BFVParameters):
        base = ceil(sqrt(params.ciph_modulus))
        num_levels = floor(log(params.ciph_modulus, base)) + 1
        
        keys = [0] * num_levels
        power = 1
        sk_squared = self.secret_key.s.multiply(self.secret_key.s, params.ciph_modulus)
        
        for i in range(num_levels):
            k1 = Polynomial(params.poly_degree, sample_uniform(0, params.ciph_modulus, params.poly_degree))
            error = Polynomial(params.poly_degree, sample_triangle(params.poly_degree))
            k0 = self.secret_key.s \
                .multiply(k1, params.ciph_modulus) \
                .add(error, params.ciph_modulus) \
                .scalar_multiply(-1) \
                .add(sk_squared.scalar_multiply(power), params.ciph_modulus) \
                .mod(params.ciph_modulus)
                
            keys[i] = (k0, k1) # type: ignore
            power *= base
            power %= params.ciph_modulus
            
        self.relin_key = BFVRelinKey(base, keys)
            
                
            
            