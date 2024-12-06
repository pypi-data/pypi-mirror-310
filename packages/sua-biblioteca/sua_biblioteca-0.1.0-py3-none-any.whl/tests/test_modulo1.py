# test_modulo1.py
import unittest
from brainthon import somar, subtrair

class TestModulo1(unittest.TestCase):
    def test_somar(self):
        self.assertEqual(somar(2, 3), 5)
        self.assertEqual(somar(-1, 1), 0)

    def test_subtrair(self):
        self.assertEqual(subtrair(5, 3), 2)
        self.assertEqual(subtrair(0, 4), -4)

if __name__ == "__main__":
    unittest.main()
