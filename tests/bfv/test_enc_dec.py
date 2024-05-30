from datetime import timedelta
import os
import unittest
from hypothesis import given, settings
from hypothesis.strategies import lists, integers, floats

from bfv.decryptor import BFVDecryptor
from bfv.encryptor import BFVEncryptor
from bfv.key_generator import BFVKeyGenerator
from bfv.parameters import BFVParameters
from util.crypto.plaintext import Plaintext
from util.polynomial import Polynomial

TEST_DIRECTORY = os.path.dirname(__file__)

class TestBFVEncDec(unittest.TestCase):
    def setUp(self):
        self.small_degree = 5
        self.small_plain_modulus = 60
        self.small_ciph_modulus = 50000
        self.large_degree = 2048
        self.large_plain_modulus = 256
        self.large_ciph_modulus = 0x3fffffff000001
        
    @given(
        lists(integers(min_value=0, max_value=59), min_size=4, max_size=4),
    )
    def test_bfv_enc_dec(self, message):
        degree = 4
        plain_modulus = 60
        ciph_modulus = 50000
        
        params = BFVParameters(degree, plain_modulus, ciph_modulus)
        key_generator = BFVKeyGenerator(params)
        encryptor = BFVEncryptor(params, key_generator.public_key)
        decryptor = BFVDecryptor(params, key_generator.secret_key)
        
        pt = Plaintext(Polynomial(degree, message))
        ct = encryptor.encrypt(pt)
        decrypted = decryptor.decrypt(ct)
        print(f"original is {str(pt)}\ndecrypted is {str(decrypted)}\n")
        self.assertEqual(str(pt), str(decrypted))

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
        
