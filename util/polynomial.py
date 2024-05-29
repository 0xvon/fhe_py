"""
Polynomial Ring Module
"""
from typing import Optional, Sequence

Vector = Sequence[int | float]

class Polynomial:
    """A polynomial in the ring R_a
    R: quotient ring Z[x]/f(x)
        where f(x) = x^d + 1

    This polynomial keeps track of the ring degree d,
    the coefficient modulus a,
    and the coefficients in an array.
    """
    def __init__(self, degree: int, coeffs: Vector):
        self.degree = degree
        assert len(coeffs) == degree, 'Polynomial size %d is not equal to %d' %(len(coeffs), degree)
        self.coeffs = coeffs

    def add(self, poly, coeff_modulus: Optional[int] = None):
        assert self.degree == poly.degree, 'Poly size is not same'
        new_coeffs = [self.coeffs[i] + poly.coeffs[i] for i in range(self.degree)]
        
        if coeff_modulus:
            new_coeffs = self.mod(new_coeffs, coeff_modulus)
            
        return Polynomial(self.degree, new_coeffs)
            

    def subtract(self, poly, coeff_modulus: Optional[int] = None):
        # inverse the polynomial
        poly = Polynomial(poly.degree, [-x for x in poly.coeffs])
        return self.add(poly, coeff_modulus)

    def multiply(self, poly, coeff_modulus: Optional[int] = None, ntt = None, crt = None):
        # TODO: impl NTT and CRT
        return self.simple_multiply(poly, coeff_modulus)

    def simple_multiply(self, poly, coeff_modulus: Optional[int] = None):
        deg = min(poly.degree, self.degree)
        new_coeffs = [0] * deg
        for d in range(2 * deg - 1): 
            index = d % deg
            sign = int(d < deg) * 2 - 1
            
            # Perform a convolution to compute the coefficient of x^d.
            coeff = 0
            for i in range(deg):
                if 0 <= d - i < deg:
                    coeff += self.coeffs[i] * poly.coeffs[d - i]
            new_coeffs[index] += sign * coeff

        if coeff_modulus:
            new_coeffs = self.mod(new_coeffs, coeff_modulus)
            
        return Polynomial(deg, new_coeffs)
                
    def divide(self, scalar: int, coeff_modulus: Optional[int] = None):
        """Divides polynomial by a scalar.
        """
        new_coeffs = [(c // scalar) for c in self.coeffs if coeff_modulus]
        
        if coeff_modulus:
            new_coeffs = self.mod(new_coeffs, coeff_modulus)
            
        return Polynomial(self.degree, new_coeffs)

    def mod(self, coeffs: Vector, coeff_modulus: int):
        return [c % coeff_modulus for c in coeffs]
        
    def rotate(self, r):
        """Rotates plaintext polynomial by r steps.
        Rotates all the plaintext coefficients to the left such that the x^r
        coefficients is now the coefficient for x^0.
        
        Applying the transformation m(X) -> m(X^k) where k = 5^r in the ciphertext polynomial.
        """
        k = 5 ** r
        new_coeffs = [0.] * self.degree
        for i in range(self.degree):
            index = (i * k) % (2 * self.degree)
            if index < self.degree:
                new_coeffs[index] = self.coeffs[i]
            else:
                new_coeffs[index - self.degree] = -self.coeffs[i]
                
        return Polynomial(self.degree, new_coeffs)
        
    def conjugate(self):
        """Conjugates plaintext coefficients.
        
        Applying the transformation m(X) -> m(X^{-1}).
        """
        new_coeffs = [0.] * self.degree
        new_coeffs[0] = self.coeffs[0]
        for i in range(1, self.degree):
            new_coeffs[i] = -self.coeffs[self.degree - i]
            
        return Polynomial(self.degree, new_coeffs)
        
    def round(self):
        """Rounds all coefficients to nearest integer.
        """
        if type(self.coeffs[0]) == complex:
            new_coeffs = [round(c.real) for c in self.coeffs]
        else:
            new_coeffs = [round(c) for c in self.coeffs]
            
        return Polynomial(self.degree, new_coeffs)
            
    def floor(self):
        """Rounds all coefficients down to the nearest integer.
        """
        new_coeffs = [int(c) for c in self.coeffs]  
        return Polynomial(self.degree, new_coeffs)
        
    def __str__(self) -> str:
        """Represents polynomial as a readable string.
        """
        s = ''
        for i in range(self.degree - 1, -1, -1):
            if self.coeffs[i] != 0:
                if s != '':
                    s += ' + '
                if i == 0 or self.coeffs[i] != 1:
                    s += str(self.coeffs[i])
                if i != 0:
                    s += 'x'
                if i > 1:
                    s += '^' + str(i)
                    
        return s