"""
    Created by: Rafal Uzarowicz
    Date of creation: 27.03.2020
    Github: https://github.com/RafalUzarowicz
"""

import unittest
from src.graph_input import read_graph_from_file
from src.graph_input import read_graph_txt
from src.graph import Graph


class TestInputFunctions(unittest.TestCase):
    def setUp(self):
        self.mockGraph = Graph()
        self.mockGraph.add_edge("A", "B", 1)
        self.mockGraph.add_edge("A", "C", 1)
        self.mockGraph.add_edge("A", "D", 8)
        self.mockGraph.add_edge("B", "D", 3)
        self.mockGraph.add_edge("C", "D", 1)
        self.mockGraph.start = "A"
        self.mockGraph.end = "D"

    def test_read_txt(self):
        graph1 = read_graph_txt(keyword_1="test", keyword_2="graph")
        lst = ["A", "B", "C", "D"]
        self.assertListEqual(list(graph1.vertices.keys()), list(self.mockGraph.vertices.keys()))
        for i in range(4):
            self.assertDictEqual(graph1.vertices[lst[i]].neighbours, self.mockGraph.vertices[lst[i]].neighbours)

    def test_read_from_file(self):
        graph1 = read_graph_from_file("../graphs/test_graph.txt")
        lst = ["A", "B", "C", "D"]
        self.assertListEqual(list(graph1.vertices.keys()), list(self.mockGraph.vertices.keys()))
        for i in range(4):
            self.assertDictEqual(graph1.vertices[lst[i]].neighbours, self.mockGraph.vertices[lst[i]].neighbours)


if __name__ == '__main__':
    unittest.main()
