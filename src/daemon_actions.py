from src.anthill import Anthill
from src.graph import Graph
from src.pheromone_update import evaporate_pheromones, single_pheromone_update


def local_search(anthill: Anthill, graph: Graph, q_param, ro_param,  diff_percent=0.5):
    if diff_percent < 0 or diff_percent > 1:
        raise ValueError("Diff_percent must be between 0 and 1")
    elif anthill is None:
        raise TypeError("No anthill given")
    else:
        evaporate_pheromones(graph, ro_param)
        best_path = anthill.get_best_ant().distance_traveled
        worst_path = anthill.get_worst_ant().distance_traveled
        len_threshold = best_path + (worst_path - best_path)*diff_percent
        for ant in anthill.ants:
            if ant.distance_traveled <= len_threshold:
                single_pheromone_update(ant, graph, q_param)