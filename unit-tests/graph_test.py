import unittest
from src.graph import Graph


class MyTestCase(unittest.TestCase):
    def test_add_edge(self):
        graph = Graph()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_edge("A", "B", 40)
        self.assertDictEqual(graph.vertices["A"].neighbours, {"B": {'weight': 40, 'pheromone': 0.001}})
        self.assertDictEqual(graph.vertices["B"].neighbours, {"A": {'weight': 40, 'pheromone': 0.001}})
        self.assertRaises(ValueError, graph.add_edge, "A", "B", -40)


if __name__ == '__main__':
    unittest.main()
