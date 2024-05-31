from math import ceil, floor, log, sqrt
import unittest
from util.math.crt import CRTContext
from util.polynomial import Polynomial
from util.tools import multiply_polynomials_rq
from util.random_sampling import sample_uniform
from hypothesis import given
from hypothesis.strategies import lists, integers, floats
import numpy as np

class TestPolynomial(unittest.TestCase):
    def setUp(self):
        self.degree = 5
        self.coeff_modulus = 60
        self.poly1 = Polynomial(self.degree, [0, 1, 4, 5, 59])
        self.poly2 = Polynomial(self.degree, [1, 2, 4, 3, 2])

    def test_add(self):
        poly_sum = self.poly1.add(self.poly2, self.coeff_modulus)
        poly_sum2 = self.poly2.add(self.poly1, self.coeff_modulus)
        self.assertEqual(poly_sum.coeffs, [1, 3, 8, 8, 1])
        self.assertEqual(poly_sum.coeffs, poly_sum2.coeffs)

    def test_subtract(self):
        poly_diff = self.poly1.subtract(self.poly2, self.coeff_modulus)
        self.assertEqual(poly_diff.coeffs, [59, 59, 0, 2, 57])

    def test_multiply(self):
        poly1 = Polynomial(4, [0, 1, 4, 5])
        poly2 = Polynomial(4, [1, 2, 4, 3])
        poly_prod = poly1.multiply(poly2, 73)
        poly_prod2 = poly2.multiply(poly1, 73)
        self.assertEqual(poly_prod.coeffs, [44, 42, 64, 17])
        self.assertEqual(poly_prod.coeffs, poly_prod2.coeffs)
        
    @given(
        lists(integers(min_value=-10000, max_value=10000) | floats(min_value=-10000, max_value=10000, allow_infinity=False, allow_nan=False), min_size=100, max_size=100),
        lists(integers(min_value=-10000, max_value=10000) | floats(min_value=-10000, max_value=10000, allow_infinity=False, allow_nan=False), min_size=100, max_size=100)
    )
    def test_multiply_fuzz(self, coeffs1, coeffs2):
        degree1 = len(coeffs1)
        degree2 = len(coeffs2)
        poly1 = Polynomial(degree1, coeffs1)
        poly2 = Polynomial(degree2, coeffs2)
        result = poly1.multiply(poly2)
        self.assertEqual(result.degree, min(degree1, degree2))
        # Compute the expected result locally using numpy
        expected_coeffs = multiply_polynomials_rq(np.array(coeffs1), np.array(coeffs2)).tolist()
        self.assertEqual(
            [round(c, 2) for c in result.coeffs],
            [round(c, 2) for c in expected_coeffs],
            f"Error: The simple multiplication result is incorrect!!!: {coeffs1} * {coeffs2} = {result.coeffs} != {expected_coeffs}"
        )
        
    @given(
        lists(integers(min_value=-10000, max_value=10000), min_size=4, max_size=4),
        lists(integers(min_value=-10000, max_value=10000), min_size=4, max_size=4)
    )
    def test_crt_multiply(self, coeffs1, coeffs2):
        log_modulus = 10
        modulus = 1 << log_modulus
        prime_size = 59
        log_poly_degree = 2
        poly_degree = 1 << log_poly_degree
        num_primes = (2 + log_poly_degree + 4 * log_modulus + prime_size - 1) // prime_size
        crt = CRTContext(num_primes, prime_size, poly_degree)
        poly1 = Polynomial(poly_degree, coeffs1)
        poly2 = Polynomial(poly_degree, coeffs2)
        poly_prod = poly1.crt_multiply(poly2, crt)
        poly_prod = poly_prod.mod_small(modulus)
        poly_prod2 = poly2.crt_multiply(poly1, crt)
        poly_prod2 = poly_prod2.mod_small(modulus)
        actual = poly1.simple_multiply(poly2, modulus)
        actual = actual.mod_small(modulus)
        print(f"{coeffs1} * {coeffs2} = {poly_prod.coeffs}")
        self.assertEqual(poly_prod.coeffs, actual.coeffs, f'CRT multiplication failed: {poly_prod.coeffs} != {actual.coeffs}')
        self.assertEqual(poly_prod.coeffs, poly_prod2.coeffs)
        
    @given(
        lists(integers(min_value=-100000, max_value=100000), min_size=128, max_size=128),
        lists(integers(min_value=-100000, max_value=100000), min_size=128, max_size=128)
    )
    def test_fft_multiply(self, coeffs1, coeffs2):
        degree1 = len(coeffs1)
        degree2 = len(coeffs2)
        poly1 = Polynomial(degree1, coeffs1)
        poly2 = Polynomial(degree2, coeffs2)
        result = poly1.fft_multiply(poly2)
        print(f"{coeffs1} * {coeffs2} = {result.coeffs}")
        expected_coeffs = multiply_polynomials_rq(np.array(coeffs1), np.array(coeffs2)).tolist()
        self.assertEqual(
            [c for c in result.coeffs],
            [c for c in expected_coeffs],
            f"Error: The simple multiplication result is incorrect!!!: {coeffs1} * {coeffs2} = {result.coeffs} != {expected_coeffs}"
        )

    def test_base_decompose(self):
        base = ceil(sqrt(self.coeff_modulus))
        num_levels = floor(log(self.coeff_modulus, base)) + 1
        poly_decomposed = self.poly1.base_decompose(base, num_levels)
        self.assertEqual(poly_decomposed[0].coeffs, [0, 1, 4, 5, 3])
        self.assertEqual(poly_decomposed[1].coeffs, [0, 0, 0, 0, 7])
        
    def test_rotate(self):
        poly1 = Polynomial(4, [0, 1, 4, 59])
        poly_rot = poly1.rotate(3)
        self.assertEqual(poly_rot.coeffs, [0, -1, 4, -59])

    def test_round(self):
        poly = Polynomial(self.degree, [0.51, -3.2, 54.666, 39.01, 0])
        poly_rounded = poly.round()
        self.assertEqual(poly_rounded.coeffs, [1, -3, 55, 39, 0])
        
    def test_str(self):
        string1 = str(self.poly1)
        string2 = str(self.poly2)
        self.assertEqual(string1, '59x^4 + 5x^3 + 4x^2 + x')
        self.assertEqual(string2, '2x^4 + 3x^3 + 4x^2 + 2x + 1')

    

if __name__ == '__main__':
    unittest.main()