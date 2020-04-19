import unittest
from src.graph import Graph
from src.graph_input import read_graph_from_file
from src.anthill import Anthill
from src.ant_colony import AntColony


class AntColonyTest(unittest.TestCase):
    def setUp(self) -> None:
        graph = Graph()
        anthill = Anthill(1)
        self.ant_colony = AntColony(anthill=anthill, graph=graph)
        self.reset_anthill()
        self.reset_graph()

    def reset_graph(self, value=0):
        self.ant_colony.graph = read_graph_from_file("../graphs/test_graph.txt")
        self.reset_pheromones(value)

    def reset_anthill(self):
        anthill = Anthill(3)
        ant = anthill.ants[0]
        ant1 = anthill.ants[1]
        ant2 = anthill.ants[2]

        ant.path = ["A", "D"]
        ant1.path = ["A", "B", "D"]
        ant2.path = ["A", "C", "D"]

        ant.distance_traveled = 8
        ant1.distance_traveled = 4
        ant2.distance_traveled = 2

        for ant in anthill.ants:
            ant.has_found = True

        self.ant_colony.anthill = anthill

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
        self.reset_anthill()

        self.ant_colony.single_pheromone_update(ant)

        self.assertEqual(graph.vertices["A"].neighbours["D"]["pheromone"], 0.125)
        self.assertEqual(graph.vertices["D"].neighbours["A"]["pheromone"], 0.125)

    def test_local_search(self):
        self.reset_anthill()
        self.reset_graph()
        self.ant_colony.q_param = 1
        self.ant_colony.ro_param = 1
        self.ant_colony.diff_percentage = 0.5
        graph = self.ant_colony.graph

        self.ant_colony.local_search()

        self.assertEqual(graph.vertices["A"].neighbours["B"]["pheromone"], 0.25)
        self.assertEqual(graph.vertices["A"].neighbours["D"]["pheromone"], 0.0)
        self.assertEqual(graph.vertices["A"].neighbours["C"]["pheromone"], 0.5)
        self.assertEqual(graph.vertices["B"].neighbours["A"]["pheromone"], 0.25)
        self.assertEqual(graph.vertices["B"].neighbours["D"]["pheromone"], 0.25)
        self.assertEqual(graph.vertices["C"].neighbours["A"]["pheromone"], 0.5)
        self.assertEqual(graph.vertices["C"].neighbours["D"]["pheromone"], 0.5)
        self.assertEqual(graph.vertices["D"].neighbours["A"]["pheromone"], 0.0)
        self.assertEqual(graph.vertices["D"].neighbours["B"]["pheromone"], 0.25)
        self.assertEqual(graph.vertices["D"].neighbours["C"]["pheromone"], 0.5)

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

    def test_pheromone_update(self):
        self.reset_graph()
        self.reset_anthill()
        graph = self.ant_colony.graph

        self.ant_colony.pheromone_update()

        self.assertEqual(graph.vertices["A"].neighbours["B"]["pheromone"], 0.25)
        self.assertEqual(graph.vertices["A"].neighbours["D"]["pheromone"], 0.125)
        self.assertEqual(graph.vertices["A"].neighbours["C"]["pheromone"], 0.5)
        self.assertEqual(graph.vertices["B"].neighbours["A"]["pheromone"], 0.25)
        self.assertEqual(graph.vertices["B"].neighbours["D"]["pheromone"], 0.25)
        self.assertEqual(graph.vertices["C"].neighbours["A"]["pheromone"], 0.5)
        self.assertEqual(graph.vertices["C"].neighbours["D"]["pheromone"], 0.5)
        self.assertEqual(graph.vertices["D"].neighbours["A"]["pheromone"], 0.125)
        self.assertEqual(graph.vertices["D"].neighbours["B"]["pheromone"], 0.25)
        self.assertEqual(graph.vertices["D"].neighbours["C"]["pheromone"], 0.5)


if __name__ == '__main__':
    unittest.main()
