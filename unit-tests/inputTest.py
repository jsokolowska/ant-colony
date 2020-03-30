import unittest
from src.graph_input import read_graph_from_file
from src.graph_input import read_graph_txt
from src.graph import Graph


class TestInputFunctions(unittest.TestCase):

    def test_read_txt(self):
        graph1 = read_graph_txt(keyword_1="test", keyword_2="Graph")
        graph2 = Graph()
        graph2.add_edge("A", "B", 1)
        graph2.add_edge("A", "C", 1)
        graph2.add_edge("B", "D", 9)
        graph2.add_edge("C", "D", 1)
        lst = ["A", "B", "C", "D"]
        self.assertListEqual(list(graph1.vertices.keys()), list(graph2.vertices.keys()))
        for i in range(4):
            self.assertDictEqual(graph1.vertices[lst[i]].neighbours, graph2.vertices[lst[i]].neighbours)

    def test_read_from_file(self):
        graph1 = read_graph_from_file("../testGraph.txt")
        graph2 = Graph()
        graph2.add_edge("A", "B", 1)
        graph2.add_edge("A", "C", 1)
        graph2.add_edge("B", "D", 9)
        graph2.add_edge("C", "D", 1)
        lst = ["A", "B", "C", "D"]
        self.assertListEqual(list(graph1.vertices.keys()), list(graph2.vertices.keys()))
        for i in range(4):
            self.assertDictEqual(graph1.vertices[lst[i]].neighbours, graph2.vertices[lst[i]].neighbours)



if __name__ == '__main__':
    unittest.main()
