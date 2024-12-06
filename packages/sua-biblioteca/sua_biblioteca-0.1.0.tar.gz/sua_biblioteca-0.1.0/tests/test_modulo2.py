# test_modulo2.py
import unittest
from brainthon import multiplicar, dividir

class TestModulo2(unittest.TestCase):
    def test_multiplicar(self):
        self.assertEqual(multiplicar(2, 3), 6)
        self.assertEqual(multiplicar(-1, 5), -5)

    def test_dividir(self):
        self.assertEqual(dividir(10, 2), 5)
        self.assertEqual(dividir(10, 0), None)

if __name__ == "__main__":
    unittest.main()
