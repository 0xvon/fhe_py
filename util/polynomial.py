"""
Polynomial Ring Module
"""
from __future__ import annotations

from typing import List, Optional, Sequence

from util.math.crt import CRTContext
from util.math.ntt import FFTContext, NTTContext

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

    def add(self, poly: Polynomial, coeff_modulus: Optional[int] = None) -> Polynomial:
        assert self.degree == poly.degree, 'Poly size is not same'
        new_coeffs = [self.coeffs[i] + poly.coeffs[i] for i in range(self.degree)]
        
        if coeff_modulus:
            new_coeffs = [c % coeff_modulus for c in new_coeffs]
            
        return Polynomial(self.degree, new_coeffs)
            

    def subtract(self, poly: Polynomial, coeff_modulus: Optional[int] = None) -> Polynomial:
        # inverse the polynomial
        poly = Polynomial(poly.degree, [-x for x in poly.coeffs])
        return self.add(poly, coeff_modulus)

    def multiply(
        self,
        poly: Polynomial,
        coeff_modulus: Optional[int] = None,
        ntt: Optional[NTTContext] = None,
        crt: Optional[CRTContext] = None,
    ) -> Polynomial:
        if crt: return self.crt_multiply(poly, crt)
        
        if ntt:
            a = ntt.ftt_fwd(self.coeffs)
            b = ntt.ftt_fwd(poly.coeffs)
            ab = [a[i] * b[i] for i in range(self.degree)]
            prod = ntt.ftt_inv(ab)
            return Polynomial(self.degree, prod)
        
        return self.simple_multiply(poly, coeff_modulus)
    
    def crt_multiply(self, poly: Polynomial, crt: CRTContext) -> Polynomial:
        poly_prods = []
        for i in range(len(crt.primes)):
            prod = self.multiply(poly, crt.primes[i], ntt=crt.ntts[i])
            poly_prods.append(prod)
            
        final_coeffs = [0] * self.degree
        for i in range(self.degree):
            values = [p.coeffs[i] for p in poly_prods]
            final_coeffs[i] = crt.reconstruct(values)
            
        return Polynomial(self.degree, final_coeffs).mod_small(crt.modulus)
    
    def fft_multiply(self, poly: Polynomial, round=True) -> Polynomial:
        """Multiplies two polynomials using FFT.
        """
        assert isinstance(poly, Polynomial)
        
        fft = FFTContext(self.degree * 8)
        a = fft.fft_fwd(self.coeffs + [0] * self.degree) # type: ignore
        b = fft.fft_fwd(poly.coeffs + [0] * self.degree) # type: ignore
        ab = [a[i] * b[i] for i in range(self.degree * 2)]
        prod = fft.fft_inv(ab)
        poly_prod = [0] * self.degree

        for d in range(2 * self.degree - 1):
            # Since x^d = -1, the degree is taken mod d, and the sign
            # changes when the exponent is > d.
            index = d % self.degree
            sign = (int(d < self.degree) - 0.5) * 2
            poly_prod[index] += sign * prod[d] # type: ignore

        if round:
            return Polynomial(self.degree, poly_prod).round()
        else:
            return Polynomial(self.degree, poly_prod)
        
    def simple_multiply(self, poly: Polynomial, coeff_modulus: Optional[int] = None) -> Polynomial:
        deg = min(poly.degree, self.degree)
        new_coeffs: List[float] = [0] * deg
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
            new_coeffs = [c % coeff_modulus for c in new_coeffs]
            
        return Polynomial(deg, new_coeffs)
    
    def scalar_multiply(self, scalar: float, coeff_modulus: Optional[int] = None) -> Polynomial:
        """Multiplies polynomial by a scalar.
        """
        if coeff_modulus:
            new_coeffs = [(c * scalar) % coeff_modulus for c in self.coeffs]
        else:
            new_coeffs = [c * scalar for c in self.coeffs]
        return Polynomial(self.degree, new_coeffs)
        
    def divide(self, scalar: int, coeff_modulus: Optional[int] = None) -> Polynomial:
        """Divides polynomial by a scalar.
        """
        new_coeffs = [(c // scalar) for c in self.coeffs if coeff_modulus]
        
        if coeff_modulus:
            new_coeffs = [c % coeff_modulus for c in new_coeffs]
            
        return Polynomial(self.degree, new_coeffs)

    def mod(self, coeff_modulus: int) -> Polynomial:
        new_coeffs = [c % coeff_modulus for c in self.coeffs]
        return Polynomial(self.degree, new_coeffs)
    
    def mod_small(self, coeff_modulus: int) -> Polynomial:
        """Turns all coefficients in the given coefficient modulus
        to the range (-q/2, q/2].

        Turns all coefficients of the current polynomial
        in the given coefficient modulus to the range (-q/2, q/2].

        Args:
            coeff_modulus (int): Modulus a of coefficients of polynomial
                ring R_a.

        Returns:
            A Polynomial whose coefficients are modulo coeff_modulus.
        """
        try:
            new_coeffs = [c % coeff_modulus for c in self.coeffs]
            new_coeffs = [c - coeff_modulus if c > coeff_modulus // 2 else c for c in new_coeffs]
        except:
            print(self.coeffs)
            print(coeff_modulus)
            new_coeffs = [c % coeff_modulus for c in self.coeffs]
            new_coeffs = [c - coeff_modulus if c > coeff_modulus // 2 else c for c in new_coeffs]
        return Polynomial(self.degree, new_coeffs)
        
    def rotate(self, r: int) -> Polynomial:
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
    
    def base_decompose(self, base: int, num_levels: int) -> list[Polynomial]:
        """Decomposes the polynomial into base.
        base (T): base to decompose coefficients into.
        num_levels: Log of ciphertext modulus with the base.
        [f(x) mod base, f(x)/base mod base, f(x)/base^2 mod base, ..., f(x)/base^(num_levels-1) mod base]
        """
        decomposed = [Polynomial(self.degree, [0] * self.degree) for _ in range(num_levels)]
        poly = self

        for i in range(num_levels):
            decomposed[i] = poly.mod(base)
            poly = poly.scalar_multiply(1 / base).floor()

        return decomposed
        
        
    def round(self) -> Polynomial:
        """Rounds all coefficients to nearest integer.
        """
        if type(self.coeffs[0]) == complex:
            new_coeffs = [round(c.real) for c in self.coeffs]
        else:
            new_coeffs = [round(c) for c in self.coeffs]
            
        return Polynomial(self.degree, new_coeffs)
            
    def floor(self) -> Polynomial:
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