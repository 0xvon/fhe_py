import unittest
import random
import matplotlib.pyplot as plt
from util.math.sign import Sign

class TestSign(unittest.TestCase):
    def test_f(self):
        n_list = range(1, 21)
        num_of_trial = 10000
        x = [random.uniform(-1, 1) for _ in range(num_of_trial)]
        cmap = plt.get_cmap('viridis', len(n_list))  # get colormap

        fig, ax = plt.subplots(figsize=(10, 8))
        for i, n in enumerate(n_list):
            sign = Sign(n)
            y = [sign.f(xi) for xi in x]
            ax.scatter(x, y, s=1, color=cmap(i), label=f'n={n}')  # set color by colormap

        ax.set_title('Sign function')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.legend()

        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    unittest.main()