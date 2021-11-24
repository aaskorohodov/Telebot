import unittest
from Processors.calc import *


class CalcTests(unittest.TestCase):

    def test_eval(self):
        self.assertEqual(calc('2+2'), 4)
        self.assertEqual(calc('2*5'), 10)
        self.assertEqual(calc('2/2'), 1.0)
        self.assertEqual(calc('2/0'), '0')
        self.assertEqual(calc('asdasd'), '"asdasd" не выражеие, я не могу такое посчитать\n'
                f'Чтобы закрыть калькулятор, напишите "все"')

    def test_type(self):
        self.assertIsInstance(calc('asd'), str)
        self.assertIsInstance(calc('2+2'), int)


if __name__ == '__main__':
    unittest.main()