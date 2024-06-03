import unittest
import matplotlib.pyplot as plt
from util.math.comparison import Comparison
from util.math.sign import Sign
import numpy as np

class TestComparison(unittest.TestCase):
    def test_comp(self):
        n = 30
        a = 0
        b_list = np.arange(-1, 1, 0.01).tolist()
        assert len(b_list) == 200

        comp = Comparison(n)
        y = [comp.comp(a, b) for b in b_list]
        
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.scatter(b_list, y, s=1, color='b')
        ax.set_title(f'Comparison function (a={a})')
        ax.set_xlabel('b')
        ax.set_ylabel('y')
        ax.set_xlim(-1, 1)
        ax.set_ylim(-0.1, 1.1)
        plt.tight_layout()
        plt.show()
        
        self.assertAlmostEqual(y[0], 1)
        self.assertAlmostEqual(y[int(len(b_list)/2)], 0.5)
        self.assertAlmostEqual(y[-1], 0)
        
    def test_max(self):
        n = 20
        a = -0.5
        b_list = np.arange(-1, 1, 0.01).tolist()
        assert len(b_list) == 200

        comp = Comparison(n)
        y = [comp.max(a, b) for b in b_list]
        ans_list = [max(a, b) for b in b_list]
        
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.scatter(b_list, y, s=1, color='b')
        ax.scatter(b_list, ans_list, s=1, color='red')
        ax.set_title(f'Max (a={a})')
        ax.set_xlabel('b')
        ax.set_ylabel(f'max({a}, b)')
        ax.set_xlim(-1, 1)
        ax.set_ylim(-0.6, 1.1)
        ax.legend(['NewMax', 'max'])
        plt.tight_layout()
        plt.show()
        
    def test_min(self):
        n = 20
        a = 0.5
        b_list = np.arange(-1, 1, 0.01).tolist()
        assert len(b_list) == 200

        comp = Comparison(n)
        y = [comp.min(a, b) for b in b_list]
        ans_list = [min(a, b) for b in b_list]
        
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.scatter(b_list, y, s=1, color='b')
        ax.scatter(b_list, ans_list, s=1, color='red')
        ax.set_title(f'Min (a={a})')
        ax.set_xlabel('b')
        ax.set_ylabel(f'min({a}, b)')
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1.1, 0.6)
        ax.legend(['NewMin', 'min'])
        plt.tight_layout()
        plt.show()
        
if __name__ == '__main__':
    unittest.main()