"""
    Created by: Rafal Uzarowicz
    Date of creation: 01.04.2020
    Github: https://github.com/RafalUzarowicz
"""

from src.generate_solutions import *


def pheromone_update(anthill: Anthill, graph: Graph):
    q_param = 1
    ro_param = 1
    for name in graph.vertices:
        for neigh in graph.vertices[name].neighbours:
            graph.vertices[name].neighbours[neigh]["pheromone"] *= 1 - ro_param
    for ant in anthill:
