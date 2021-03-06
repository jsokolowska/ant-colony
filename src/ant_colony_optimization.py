"""
    Created by: Rafal Uzarowicz, Joanna Sokolowska
    Date of creation: 19.04.2020
    Github: https://github.com/RafalUzarowicz https://github.com/jsokolowska
"""

from src.graph import Graph
from src.anthill import Anthill
from src.graph_input import read_graph_txt
from random import uniform
import copy


class AntColonyOptimization:
    def __init__(self, *, anthill: Anthill = None, graph: Graph = None, q_param=1, ro_param=0.4, alpha_param=1,
                 beta_param=1, persistence_param=5, ants_num=50, ls_flag=True, diff_percentage=0.3):
        if type(graph) is not Graph:
            self.graph = read_graph_txt()
        else:
            self.graph = graph
        if type(anthill) is not Anthill:
            self.anthill = Anthill(ants_num)
        else:
            self.anthill = anthill
        self.q_param = q_param
        self.ro_param = ro_param
        self.alpha_param = alpha_param
        self.beta_param = beta_param
        self.ls_flag = ls_flag
        self.diff_percentage = diff_percentage
        self.persistence_param = persistence_param

    def run(self, iterations_limit: int = 1000) -> ([], int):
        if type(self.anthill) is not Anthill or type(self.graph) is not Graph:
            raise TypeError("Graph or anthill have wrong types.")
        if len(self.graph.vertices) <= 0 or self.graph.start is None or self.graph.end is None:
            raise ValueError("Vertices not set up properly.")
        if iterations_limit <= 0:
            raise ValueError("Number of iterations must be greater than 0")
        all_iterations_counter = 0
        worse_repeat_limit_counter = 0
        curr_best_path_distance = 0
        best_path_distance = 0
        best_ant = Anthill.Ant()
        best_ant.distance_traveled = 0
        while all_iterations_counter < iterations_limit and worse_repeat_limit_counter < self.persistence_param - 1:
            best_path_distance = curr_best_path_distance
            self.generate_solutions()
            curr_best_ant = self.anthill.get_best_ant()
            if best_ant.distance_traveled > curr_best_ant.distance_traveled > 0 or best_ant.distance_traveled == 0:
                best_ant = copy.deepcopy(curr_best_ant)
            curr_best_path_distance = curr_best_ant.distance_traveled
            if all_iterations_counter and curr_best_path_distance >= best_path_distance:
                if curr_best_path_distance:
                    worse_repeat_limit_counter += 1
                if best_path_distance > 0:
                    self.alpha_param *= 1 + 1/best_path_distance
                    self.beta_param *= 1 - 1/best_path_distance
            else:
                worse_repeat_limit_counter = 0
                if best_path_distance > 0:
                    self.alpha_param *= 1 - 1 / best_path_distance
                    self.beta_param *= 1 + 1 / best_path_distance
            if self.ls_flag:
                self.local_search()
            else:
                self.pheromone_update()
            all_iterations_counter += 1
        if best_ant is not None:
            path = (best_ant.path, best_ant.distance_traveled)
            return path
        else:
            return None, None

    def generate_solutions(self):
        self.anthill.reset_ants()
        vertex_lst = list(self.graph.vertices.keys())
        vertex_lst.remove(self.graph.start)
        for ant in self.anthill.ants:
            unvisited_vertex_lst = vertex_lst.copy()
            ant.path.append(self.graph.start)
            curr_vertex = self.graph.start
            while True:
                if curr_vertex == self.graph.end:
                    ant.has_found = True
                    break
                prev_vertex = curr_vertex
                available_vertices = {k: v for k, v in self.graph.vertices[curr_vertex].neighbours.items() if
                                      k in unvisited_vertex_lst}
                curr_vertex = self.pick_vertex(available_vertices)
                if curr_vertex is None or not len(available_vertices):
                    ant.has_found = False
                    break
                ant.path.append(curr_vertex)
                unvisited_vertex_lst.remove(curr_vertex)
                ant.distance_traveled += self.graph.vertices[prev_vertex].neighbours[curr_vertex]["weight"]

    def pick_vertex(self, neighbours: {}):
        tau = [[k, ((1 / v["weight"]) ** self.beta_param) * (v["pheromone"] ** self.alpha_param)] for k, v in
               neighbours.items()]
        if not len(tau):
            return None
        total = 0
        for val in tau:
            total += val[1]
        if total == 0.0:
            tau = [[k, (1 / v["weight"])] for k, v in neighbours.items()]
            for val in tau:
                total += val[1]
        for i in range(len(tau)):
            tau[i][1] /= total
        curr = 1.0
        i = -1
        rand_number = uniform(0, 1)
        while i < len(tau) - 1 and rand_number < curr:
            i += 1
            curr -= tau[i][1]
        return tau[i][0]

    def single_pheromone_update(self, ant):
        if ant.has_found and ant.distance_traveled > 0.0:
            new_pheromone = self.q_param / ant.distance_traveled
            for i in range(len(ant.path) - 1):
                self.graph.vertices[ant.path[i]].neighbours[ant.path[i + 1]]["pheromone"] += new_pheromone
                self.graph.vertices[ant.path[i + 1]].neighbours[ant.path[i]]["pheromone"] += new_pheromone

    def evaporate_pheromones(self):
        for vertex in self.graph.vertices:
            for neighbour in self.graph.vertices[vertex].neighbours:
                self.graph.vertices[vertex].neighbours[neighbour]["pheromone"] *= 1 - self.ro_param

    def pheromone_update(self):
        self.evaporate_pheromones()
        for ant in self.anthill.ants:
            self.single_pheromone_update(ant)

    def local_search(self):
        if self.diff_percentage < 0 or self.diff_percentage > 1:
            raise ValueError("Diff_percent must be between 0 and 1")
        else:
            self.evaporate_pheromones()
            best_path = self.anthill.get_best_ant().distance_traveled
            worst_path = self.anthill.get_worst_ant().distance_traveled
            len_threshold = best_path + (worst_path - best_path) * self.diff_percentage
            for ant in self.anthill.ants:
                if ant.distance_traveled <= len_threshold:
                    self.single_pheromone_update(ant)
