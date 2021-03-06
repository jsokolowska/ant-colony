import unittest
from src.anthill import Anthill


class AnthillTest(unittest.TestCase):
    def test_get_best_ant(self):
        anthill = Anthill(10)
        for i in range(10):
            anthill.ants[i].distance_traveled = i**2
            anthill.ants[i].has_found = True

        best_ant = anthill.get_best_ant()
        self.assertEqual(best_ant.distance_traveled, 0)

        anthill.ants = []
        self.assertIsNone(anthill.get_best_ant())

    def test_get_worst_ant(self):
        anthill = Anthill(10)
        for i in range(10):
            anthill.ants[i].distance_traveled = i ** 2
            anthill.ants[i].has_found = True

        worst_ant = anthill.get_worst_ant()
        self.assertEqual(worst_ant.distance_traveled, 81)

        anthill.ants = []
        self.assertIsNone(anthill.get_worst_ant())


if __name__ == '__main__':
    unittest.main()
