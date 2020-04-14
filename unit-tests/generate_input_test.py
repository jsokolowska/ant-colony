import unittest
from os.path import isfile
from src.generate_input import generate_input


class GenerateInputTest(unittest.TestCase):
    def test_generate_input(self):
        filename = "test_graph_auto.txt"
        filepath = "../graphs/" + filename
        vertices = 20
        density = 0.7

        generate_input(vertices, density, filename)

        self.assertTrue(isfile(filepath))
        self.assertRaises(ValueError, generate_input, -10, 0.5)
        self.assertRaises(ValueError, generate_input, 10, -1)
        self.assertRaises(ValueError, generate_input, 10, 2)


if __name__ == '__main__':
    unittest.main()
