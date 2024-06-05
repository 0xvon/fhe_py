from datetime import timedelta
import os
from typing import List
import unittest
from ckks.encoder import CKKSEncoder
from hypothesis import given, settings
from hypothesis.strategies import lists, integers, complex_numbers

from ckks.decryptor import CKKSDecryptor
from ckks.encryptor import CKKSEncryptor
from ckks.key_generator import CKKSKeyGenerator
from ckks.parameters import CKKSParameters

from bfv.decryptor import BFVDecryptor
from bfv.encryptor import BFVEncryptor
from bfv.key_generator import BFVKeyGenerator
from bfv.parameters import BFVParameters
from util.crypto.plaintext import Plaintext
from util.polynomial import Polynomial
from util.random_sampling import sample_random_complex_vector

TEST_DIRECTORY = os.path.dirname(__file__)

class TestBFVEncDec(unittest.TestCase):
    def setUp(self):
        self.small_degree = 5
        self.small_plain_modulus = 60
        self.small_ciph_modulus = 50000
        self.large_degree = 2048
        self.large_plain_modulus = 256
        self.large_ciph_modulus = 0x3fffffff000001

    @settings(deadline=timedelta(seconds=60))
    @given(
        lists(integers(min_value=0, max_value=255), min_size=2048, max_size=2048),
    )
    def test_bfv_enc_dec_large(self, message):
        degree = 2048
        plain_modulus = 256
        ciph_modulus = 0x3fffffff000001
        
        params = BFVParameters(degree, plain_modulus, ciph_modulus)
        key_generator = BFVKeyGenerator(params)
        encryptor = BFVEncryptor(params, key_generator.public_key)
        decryptor = BFVDecryptor(params, key_generator.secret_key)
        
        pt = Plaintext(Polynomial(degree, message))
        ct = encryptor.encrypt(pt)
        decrypted = decryptor.decrypt(ct)
        print(f"original is {str(pt)}\ndecrypted is {str(decrypted)}\n")
        self.assertEqual(str(pt), str(decrypted))
        
class TestCKKSEncDec(unittest.TestCase):
    def setUp(self):
        self.poly_degree = 64
        self.ciph_modulus = 1 << 1200
        self.big_modulus = 1 << 1200
        self.scaling_factor = 1 << 30
        self.error = 0.00001
    
    def ckks_enc_dec(self, message: List[complex]):
        params = CKKSParameters(self.poly_degree, self.ciph_modulus, self.big_modulus, self.scaling_factor)
        key_generator = CKKSKeyGenerator(params)
        encryptor = CKKSEncryptor(params, key_generator.public_key)
        decryptor = CKKSDecryptor(params, key_generator.secret_key)
        encoder = CKKSEncoder(params)
        pt = encoder.encode(message, self.scaling_factor)        
        ct = encryptor.encrypt(pt)
        decrypted = decryptor.decrypt(ct)
        decoded = encoder.decode(decrypted)
        for i in range(len(message)):
            print(f"comparing {message[i]} and {decoded[i]}...")
            print(f"real part diff: {abs(message[i].real - decoded[i].real)}")
            print(f"img part diff: {abs(message[i].imag - decoded[i].imag)}")
            self.assertTrue(abs(message[i].real - decoded[i].real) < self.error)
            self.assertTrue(abs(message[i].imag - decoded[i].imag) < self.error)
        
    def test_ckks_enc_dec(self):
        attempts = 1000
        for _ in range(attempts):
            message = sample_random_complex_vector(self.poly_degree // 2)
            self.ckks_enc_dec(message)
