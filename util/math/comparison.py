from typing import List
from util.math.sign import Sign

class Comparison:
    def __init__(self, n: int):
        """Inits Comparison with a and b.
        Ref: https://eprint.iacr.org/2019/1234
        """
        self.sign = Sign(n)

    def comp(self, a: float, b: float) -> float:
        """Compares two numbers a and b.
        Returns 1 if a > b, 0 if a = b, -1 if a < b.
        Ref: https://eprint.iacr.org/2019/1234, pp. 16, Algorithm 1 NewComp
        """
        diff = a - b
        return (self.sign.f(diff) + 1) / 2
    
    def max(self, a: float, b: float) -> float:
        """Returns the maximum of two numbers a and b.
        Ref: https://eprint.iacr.org/2019/1234, pp. 24, Algorithm 4 NewMax
        """
        x = a - b
        y = (a + b) / 2
        x = self.sign.f(x)
        return y + (a - b) / 2 * x
    
    def min(self, a: float, b: float) -> float:
        """Returns the minimum of two numbers a and b.
        Ref: https://eprint.iacr.org/2019/1234, pp. 24, Algorithm 4 NewMax
        """
        x = a - b
        y = (a + b) / 2
        x = self.sign.f(x)
        return y - (a - b) / 2 * x