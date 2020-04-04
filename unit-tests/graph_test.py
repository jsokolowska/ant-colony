import unittest
from src.graph import Graph


class MyTestCase(unittest.TestCase):
    def test_add_edge(self):
        graph = Graph()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_edge("A", "B", 40)
        self.assertDictEqual(graph.vertices["A"].neighbours, {"B": 40})
        self.assertDictEqual(graph.vertices["B"].neighbours, {"A": 40})
        self.assertRaises(ValueError, graph.add_edge, "A", "B", -40)
        # self.assertRaises(IndexError, graph.add_edge, 20, 4, 10)


if __name__ == '__main__':
    unittest.main()
