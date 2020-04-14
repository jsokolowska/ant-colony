import unittest
from src.graph import Graph
from src.pheromone_update import evaporate_pheromones, single_pheromone_update
from src.anthill import Anthill
from src.daemon_actions import local_search


class acoTest(unittest.TestCase):
    def test_evaporate_pheromones(self):
        graph = Graph()
        graph.add_edge("A", "B", weight=1, pheromone=1)
        evaporate_pheromones(graph, 1)
        self.assertEqual(graph.vertices["A"].neighbours["B"]["pheromone"], 0.0)
        self.assertEqual(graph.vertices["B"].neighbours["A"]["pheromone"], 0.0)

        graph.add_edge("C", "A", weight=1, pheromone=1)
        evaporate_pheromones(graph, 0.5)
        self.assertEqual(graph.vertices["A"].neighbours["C"]["pheromone"], 0.5)
        self.assertEqual(graph.vertices["C"].neighbours["A"]["pheromone"], 0.5)

    def test_single_pheromone_update(self):
        anthill = Anthill(1)
        ant = anthill.ants[0]
        ant.path = ["A", "B"]
        ant.has_found = True
        ant.distance_traveled = 1

        graph = Graph()
        graph.add_edge("A", "B", weight=1, pheromone=1)
        single_pheromone_update(ant, graph, q_param=1)
        self.assertEqual(graph.vertices["A"].neighbours["B"]["pheromone"], 2.0)
        self.assertEqual(graph.vertices["B"].neighbours["A"]["pheromone"], 2.0)

    def test_local_search(self):
        anthill = Anthill(3)
        anthill.ants[0].path = ["A", "B"]
        anthill.ants[1].path = ["A", "C", "A", "B"]
        anthill.ants[2].path = ["A", "B"]

        anthill.ants[0].distance_traveled = 2
        anthill.ants[1].distance_traveled = 8
        anthill.ants[2].distance_traveled = 4
        for ant in anthill.ants:
            ant.has_found = True

        graph = Graph()
        graph.add_edge("A", "B", weight=1, pheromone=0.0)
        graph.add_edge("A", "C", weight=1, pheromone=0.0)

        local_search(anthill, graph, ro_param=1, q_param=1, diff_percent=0.5)

        self.assertEqual(graph.vertices["C"].neighbours["A"]["pheromone"], 0.0)
        self.assertEqual(graph.vertices["A"].neighbours["C"]["pheromone"], 0.0)
        self.assertNotEqual(graph.vertices["A"].neighbours["B"]["pheromone"], 0.0)
        self.assertNotEqual(graph.vertices["B"].neighbours["A"]["pheromone"], 0.0)


if __name__ == '__main__':
    unittest.main()
