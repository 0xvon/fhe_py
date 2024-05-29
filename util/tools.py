from typing import Optional
import numpy as np

def multiply_polynomials_rq(a: np.ndarray, b: np.ndarray, q: Optional[int] =None):
    """Multiplies two polynomials in the ring R_q using numpy.

    Args:
        a (numpy.ndarray): Coefficients of the first polynomial.
        b (numpy.ndarray): Coefficients of the second polynomial.
        q (int): Modulus for the coefficients in the ring R_q.

    Returns:
        numpy.ndarray: Coefficients of the product polynomial in R_q.
    """
    n = len(a)
    assert len(b) == n, "Both polynomials must have the same degree."

    # Perform the convolution
    conv_result = np.convolve(a, b)

    # Initialize the resulting polynomial coefficients
    poly_prod = np.zeros(n, dtype=float)

    for d in range(2 * n - 1):
        index = d % n
        sign = 1 if d < n else -1

        poly_prod[index] += sign * conv_result[d]

    # Apply modulus q
    if q:
        poly_prod %= q

    return poly_prod