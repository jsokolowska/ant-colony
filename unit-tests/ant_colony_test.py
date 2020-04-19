import unittest
from src.graph import Graph
from src.graph_input import read_graph_from_file
# from src.pheromone_update import pheromone_update
# from src.generate_solutions import generate_solutions
# from src.pheromone_update import evaporate_pheromones, single_pheromone_update
from src.anthill import Anthill
# from src.daemon_actions import local_search
from src.ant_colony import AntColony


class AntColonyTest(unittest.TestCase):
    def setUp(self) -> None:
        graph = Graph()
        graph.add_edge("A", "B", weight=1, pheromone=1)
        graph.add_edge("C", "A", weight=1, pheromone=1)

        anthill = Anthill(3)
        ant = anthill.ants[0]
        ant1 = anthill.ants[1]
        ant2 = anthill.ants[2]

        ant.path = ["A", "B"]
        ant1.path = ["A", "C", "A", "B"]
        ant2.path = ["A", "B"]
        ant.distance_traveled = 1
        ant1.distance_traveled = 8
        ant2.distance_traveled = 3
        for ant in anthill.ants:
            ant.has_found = True

        self.ant_colony = AntColony(anthill=anthill, graph=graph)

    def reset_pheromones(self, value=0):
        for vertex in self.ant_colony.graph.vertices:
            for neighbour in self.ant_colony.graph.vertices[vertex].neighbours:
                self.ant_colony.graph.vertices[vertex].neighbours[neighbour]["pheromone"] = 0

    def test_evaporate_pheromones(self):
        graph = self.ant_colony.graph
        self.ant_colony.ro_param = 1
        self.reset_pheromones()

        self.ant_colony.evaporate_pheromones()

        self.assertEqual(graph.vertices["A"].neighbours["B"]["pheromone"], 0.0)
        self.assertEqual(graph.vertices["B"].neighbours["A"]["pheromone"], 0.0)
        self.assertEqual(graph.vertices["C"].neighbours["A"]["pheromone"], 0.0)
        self.assertEqual(graph.vertices["A"].neighbours["C"]["pheromone"], 0.0)

    def test_single_pheromone_update(self):
        graph = self.ant_colony.graph
        ant = self.ant_colony.anthill.ants[0]
        self.ant_colony.q_param = 1
        self.reset_pheromones()

        self.ant_colony.single_pheromone_update(ant)

        self.assertEqual(graph.vertices["A"].neighbours["B"]["pheromone"], 1.0)
        self.assertEqual(graph.vertices["B"].neighbours["A"]["pheromone"], 1.0)

    def test_local_search(self):
        self.reset_pheromones()
        self.ant_colony.q_param = 1
        self.ant_colony.ro_param = 1
        self.ant_colony.diff_percentage = 0.5
        graph = self.ant_colony.graph

        self.ant_colony.local_search()

        self.assertEqual(graph.vertices["C"].neighbours["A"]["pheromone"], 0.0)
        self.assertEqual(graph.vertices["A"].neighbours["C"]["pheromone"], 0.0)
        self.assertNotEqual(graph.vertices["A"].neighbours["B"]["pheromone"], 0.0)
        self.assertNotEqual(graph.vertices["B"].neighbours["A"]["pheromone"], 0.0)

        self.ant_colony.diff_percentage = -1
        self.assertRaises(ValueError, self.ant_colony.local_search )
        self.ant_colony.diff_percentage = -2
        self.assertRaises(ValueError, self.ant_colony.local_search)

    def test_run(self):
        self.ant_colony.anthill = None
        self.assertRaises(TypeError, self.ant_colony.run)

        self.ant_colony.anthill = Anthill(1)
        self.ant_colony.graph = None
        self.assertRaises(TypeError, self.ant_colony.run)

        self.ant_colony.graph = Graph()
        self.ant_colony.graph.end = 'o'
        self.ant_colony.graph.start = 'a'
        self.assertRaises(ValueError, self.ant_colony.run)

        self.ant_colony.graph.add_edge('a', 'b', 1)
        self.ant_colony.graph.end = None
        self.assertRaises(ValueError, self.ant_colony.run)

        self.ant_colony.graph.start = None
        self.ant_colony.graph.end = 'o'
        self.assertRaises(ValueError, self.ant_colony.run)

        self.ant_colony.graph.start = 'a'
        self.assertRaises(ValueError, self.ant_colony.run, -3)

    # def test_pheromone_update(self):
        # self.ant_colony.graph = read_graph_from_file("../graphs/test_graph.txt")
        # graph = self.ant_colony.graph
        # graph.vertices["A"].neighbours["C"]["pheromone"] = 1
        # self.reset_pheromones(1)
        # self.ant_colony.ro_param = 0.5
        # self.ant_colony.q_param = 1
        # #self.ant_colony.anthill = Anthill(2)
        # # anthill = Anthill(2)
        # # graph = Graph()
        # #
        # # self.assertRaises(TypeError, pheromone_update, anthill, 1)
        # # self.assertRaises(TypeError, pheromone_update, 1, graph)
        # # self.assertRaises(ValueError, pheromone_update, anthill, graph)
        # #
        # # graph = read_graph_txt(keyword_1="test", keyword_2="graph")
        # # graph.vertices["A"].neighbours["C"]["pheromone"] = 1
        # # for key in graph.vertices:
        # #     for neigh in graph.vertices[key].neighbours:
        # #         graph.vertices[key].neighbours[neigh]["pheromone"] = 1
        # #
        # # pheromone_update(anthill, graph)
        # #
        # self.ant_colony.pheromone_update()
        # for key in graph.vertices:
        #     for neigh in graph.vertices[key].neighbours:
        #         self.assertEqual(graph.vertices[key].neighbours[neigh]["pheromone"], 0.5)
        # #
        # # anthill.ants[0].path = ["A", "C", "D"]
        # # anthill.ants[0].has_found = True
        # # anthill.ants[0].distance_traveled = 2
        # # anthill.ants[1].path = ["A", "B", "D"]
        # # anthill.ants[1].has_found = True
        # # anthill.ants[1].distance_traveled = 10
        # #
        # # for key in graph.vertices:
        # #     for neigh in graph.vertices[key].neighbours:
        # #         graph.vertices[key].neighbours[neigh]["pheromone"] = 1
        # #
        # # pheromone_update(anthill, graph)
        # #
        # # self.assertEqual(graph.vertices["A"].neighbours["C"]["pheromone"], 1)
        # # self.assertEqual(graph.vertices["C"].neighbours["A"]["pheromone"], 1)
        # # self.assertEqual(graph.vertices["A"].neighbours["B"]["pheromone"], 0.6)
        # # self.assertEqual(graph.vertices["B"].neighbours["A"]["pheromone"], 0.6)
        # # self.assertEqual(graph.vertices["C"].neighbours["D"]["pheromone"], 1)
        # # self.assertEqual(graph.vertices["D"].neighbours["C"]["pheromone"], 1)
        # # self.assertEqual(graph.vertices["D"].neighbours["B"]["pheromone"], 0.6)
        # # self.assertEqual(graph.vertices["B"].neighbours["D"]["pheromone"], 0.6)

if __name__ == '__main__':
    unittest.main()
