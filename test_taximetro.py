import unittest

class TestTaximetro(unittest.TestCase):
    def test_calculo_tarifa(self):
        # Prueba: 10 segundos parado (10 * 0.02 = 0.20)
        # y 10 segundos en marcha (10 * 0.05 = 0.50)
        # Total esperado: 0.70
        parado = 10 * 0.02
        marcha = 10 * 0.05
        total = parado + marcha
        self.assertEqual(total, 0.70)

if __name__ == '__main__':
    unittest.main()