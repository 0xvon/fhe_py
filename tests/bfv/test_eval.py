from datetime import timedelta
import unittest
from bfv.decryptor import BFVDecryptor
from bfv.encryptor import BFVEncryptor
from bfv.evaluator import BFVEvaluator
from bfv.key_generator import BFVKeyGenerator
from bfv.parameters import BFVParameters
from bfv.relin_key import BFVRelinKey
from util.crypto.ciphertext import Ciphertext
from util.crypto.plaintext import Plaintext
from util.polynomial import Polynomial
from hypothesis import HealthCheck, given, settings
from hypothesis.strategies import lists, integers

class TestBFVEvaluator(unittest.TestCase):
    def setUp(self):
        self.params = BFVParameters(5, 60, 73)
        self.evaluator = BFVEvaluator(self.params)
        self.relin_key = BFVRelinKey(keys=[(Polynomial(5, [1, 2, 3, 4, 5]), Polynomial(5, [5, 4, 3, 2, 1]))], base=2)

    @given(
        lists(integers(min_value=0, max_value=59), min_size=4, max_size=4),
        lists(integers(min_value=0, max_value=59), min_size=4, max_size=4),
    )
    def test_homomorphic_add(self, m1, m2):
        degree = 4
        plain_modulus = 60
        ciph_modulus = 50000
        
        params = BFVParameters(degree, plain_modulus, ciph_modulus)
        key_generator = BFVKeyGenerator(params)
        encryptor = BFVEncryptor(params, key_generator.public_key)
        evaluator = BFVEvaluator(params)
        decryptor = BFVDecryptor(params, key_generator.secret_key)
        
        a = Plaintext(Polynomial(degree, m1))
        ct1 = encryptor.encrypt(a)
        b = Plaintext(Polynomial(degree, m2))
        ct2 = encryptor.encrypt(b)
        ct_add = evaluator.add(ct1, ct2)
        decrypted = decryptor.decrypt(ct_add)
        answer = Polynomial(degree, [m1[i] + m2[i] for i in range(degree)]).mod(plain_modulus)
        print(f"{m1} + {m2} = {decrypted.poly} (answer:{answer})")
        self.assertEqual(str(decrypted.poly), str(answer))

    @settings(deadline=timedelta(seconds=60), suppress_health_check=[HealthCheck.large_base_example])
    @given(
        lists(integers(min_value=0, max_value=255), min_size=2048, max_size=2048),
        lists(integers(min_value=0, max_value=255), min_size=2048, max_size=2048),
    )
    def test_homomorphic_add_large(self, m1, m2):
        degree = 2048
        plain_modulus = 256
        ciph_modulus = 0x3fffffff000001
        
        params = BFVParameters(degree, plain_modulus, ciph_modulus)
        key_generator = BFVKeyGenerator(params)
        encryptor = BFVEncryptor(params, key_generator.public_key)
        evaluator = BFVEvaluator(params)
        decryptor = BFVDecryptor(params, key_generator.secret_key)
        
        a = Plaintext(Polynomial(degree, m1))
        ct1 = encryptor.encrypt(a)
        b = Plaintext(Polynomial(degree, m2))
        ct2 = encryptor.encrypt(b)
        ct_add = evaluator.add(ct1, ct2)
        decrypted = decryptor.decrypt(ct_add)
        answer = Polynomial(degree, [m1[i] + m2[i] for i in range(degree)]).mod(plain_modulus)
        print(f"{m1} + {m2} = {decrypted.poly} (answer: {answer})")
        self.assertEqual(str(decrypted.poly), str(answer))

    @settings(deadline=timedelta(seconds=60), suppress_health_check=[HealthCheck.large_base_example])
    @given(
        lists(integers(min_value=0, max_value=255), min_size=512, max_size=512),
        lists(integers(min_value=0, max_value=255), min_size=512, max_size=512),
    )
    def test_homomorphic_mul(self, m1, m2):
        degree = 512
        plain_modulus = 256
        ciph_modulus = 0x3fffffff000001
        
        params = BFVParameters(degree, plain_modulus, ciph_modulus)
        key_generator = BFVKeyGenerator(params)
        encryptor = BFVEncryptor(params, key_generator.public_key)
        evaluator = BFVEvaluator(params)
        decryptor = BFVDecryptor(params, key_generator.secret_key)
        
        a = Polynomial(degree, m1)
        pt1 = Plaintext(a)
        ct1 = encryptor.encrypt(pt1)
        b = Polynomial(degree, m2)
        pt2 = Plaintext(b)
        ct2 = encryptor.encrypt(pt2)
        ct_add = evaluator.multiply(ct1, ct2, key_generator.relin_key)
        decrypted = decryptor.decrypt(ct_add)
        answer = a.multiply(b, plain_modulus)
        print(f"{m1} * {m2} = {decrypted.poly} (answer: {answer})")
        self.assertEqual(str(decrypted.poly), str(answer))

if __name__ == '__main__':
    unittest.main()