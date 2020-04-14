"""
    Created by: Rafal Uzarowicz
    Date of creation: 27.03.2020
    Github: https://github.com/RafalUzarowicz
"""

import unittest
from src.path_search_algo import dijkstra, brute_force, choose_shortest_path
from src.graph import Graph


class TestPathSearchAlgorithms(unittest.TestCase):

    def test_dijkstra(self):
        graph = Graph()
        graph.add_edge("A", "B", 1)
        graph.add_edge("A", "C", 1)
        graph.add_edge("B", "D", 9)
        graph.add_edge("C", "D", 1)
        path, distance = dijkstra(graph,"A", "D")
        self.assertListEqual(path, ["A", "C", "D"])
        self.assertEqual(distance, 2)
        self.assertRaises(ValueError, dijkstra, graph, "A", "X")
        self.assertRaises(TypeError, dijkstra, "A", 7)

    def test_brute_force(self):
        graph1 = Graph()
        graph1.add_edge("A", "B", 1)
        graph1.add_edge("A", "C", 1)
        graph1.add_edge("B", "D", 9)
        graph1.add_edge("C", "D", 1)
        graph1.set_end_vertex("D")
        graph1.set_start_vertex("A")
        path = brute_force(graph1)
        self.assertListEqual(path[0], ["A", "C", "D"])
        self.assertEqual(path[1], 2)

    def test_choose_shortest_path(self):
        self.assertIsNone(choose_shortest_path(None))

        paths = [([], 1), ([], 2), ([], 8)]
        result = choose_shortest_path(paths)
        self.assertEqual(result[1], 1)

        paths.append(([], 0.5))
        result = choose_shortest_path(paths)
        self.assertEqual(result[1], 0.5)


if __name__ == '__main__':
    unittest.main()
