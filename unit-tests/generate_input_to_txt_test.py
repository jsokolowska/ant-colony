import unittest
from os.path import isfile
from src.generate_input import generate_input_to_txt


class GenerateInputTest(unittest.TestCase):
    def test_generate_input_to_txt(self):
        filename = "test_graph_auto.txt"
        filepath = "../graphs/" + filename
        vertices = 20
        density = 0.7

        generate_input_to_txt(vertices, density, filename)

        self.assertTrue(isfile(filepath))
        self.assertRaises(ValueError, generate_input_to_txt, -10, 0.5, filename)
        self.assertRaises(ValueError, generate_input_to_txt, 10, -1, filename)
        self.assertRaises(ValueError, generate_input_to_txt, 10, 2, filename)


if __name__ == '__main__':
    unittest.main()
