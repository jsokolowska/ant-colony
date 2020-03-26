import unittest
from graph import Graph


class MyTestCase(unittest.TestCase):
    def test_add_edge(self):
        graph = Graph()
        graph.add_vertex(2)
        graph.add_edge(0, 1, 40)
        self.assertDictEqual(graph.vertices[0], {1: 40})
        self.assertDictEqual(graph.vertices[1], {0: 40})
        self.assertRaises(ValueError, graph.add_edge, 0, 1, -40)
        self.assertRaises(IndexError, graph.add_edge, 20, 4, 10)


if __name__ == '__main__':
    unittest.main()
