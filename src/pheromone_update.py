"""
    Created by: Rafal Uzarowicz
    Date of creation: 01.04.2020
    Github: https://github.com/RafalUzarowicz
"""

from src.graph import Graph
from src.anthill import Anthill


def pheromone_update(anthill: Anthill, graph: Graph):
    q_param = 1
    ro_param = 1
    for name in graph.vertices:
        for neigh in graph.vertices[name].neighbours:
            graph.vertices[name].neighbours[neigh]["pheromone"] *= 1 - ro_param
    for ant in anthill:
        if ant.has_found:
            for i in range(len(ant.path)-1):
                pheromone_new = q_param / ant.distance_traveled
                graph.vertices[ant.path[i]].neighbours[ant.path[i + 1]]["pheromone"] += pheromone_new
                graph.vertices[ant.path[i + 1]].neighbours[ant.path[i]]["pheromone"] += pheromone_new
