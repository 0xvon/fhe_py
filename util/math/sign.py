import math
from typing import List

class Sign:
    def __init__(self, n: int):
        """Inits Sign with the number of terms.
        Define f(x) which is the approximation function 
            for sign(x) = 1 if x > 0, 0 if x = 0, -1 if x < 0.
        f(x) = Σ (1/4^i) * C(2i, i) * x(1-x^2)^i
        Ref: https://eprint.iacr.org/2019/1234, pp.12
        """
        result: List[float] = [0] * ((n + 1) * 2)
        for i in range(n + 1):
            term: float = (1 / (4 ** i)) * math.comb(2 * i, i)
            # add term for (1-x^2)^i
            for k in range(i + 1):
                unit = (-1) ** k
                result[2 * k + 1] += term * unit * math.comb(i, k)
        self.n = n
        self.coeffs = result

    def f(self, x: float) -> float:
        result = 0
        degree = len(self.coeffs)
        for i in range(degree):
            result += self.coeffs[i] * x ** i
        return result