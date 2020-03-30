"""
    Created by: Rafal Uzarowicz
    Date of creation: 27.03.2020
    Github: https://github.com/RafalUzarowicz
"""

import unittest
from src.path_search_algo import dijkstra
from src.graph import Graph


class TestPathSearchAlgorithms(unittest.TestCase):

    def test_dijkstra(self):
        graph= Graph()
        graph.add_edge("A", "B", 1)
        graph.add_edge("A", "C", 1)
        graph.add_edge("B", "D", 9)
        graph.add_edge("C", "D", 1)
        path = dijkstra(graph,"A", "D")
        self.assertListEqual(path, ["A", "C", "D"])
        self.assertRaises(ValueError, dijkstra, graph, "A", "X")
        self.assertRaises(TypeError, dijkstra, "A", 7)

if __name__ == '__main__':
    unittest.main()