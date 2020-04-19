from src.graph import Graph
from src.anthill import Anthill
from src.graph_input import read_graph_txt
from src.vertex import Vertex
from random import uniform


class AntColony:
    def __init__(self, *, anthill: Anthill = None, graph: Graph = None, q_param=1, ro_param=0.5, alpha_param=1,
                 beta_param=1, ants_num=50, ls_flag=True, diff_percentage=0.5):
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

    def run(self, iterations: int = 20):
        if type(self.anthill) is not Anthill or type(self.graph) is not Graph:
            raise TypeError("Graph or anthill have wrong types.")
        if len(self.graph.vertices) <= 0 or self.graph.start is None or self.graph.end is None:
            raise ValueError("Vertices not set up properly.")
        if iterations <= 0:
            raise ValueError("Number of iterations must be greater than 0")

        for i in range(iterations):
            self.generate_solutions()
            if self.ls_flag:
                self.local_search()
            else:
                self.pheromone_update()

    def generate_solutions(self):
        self.anthill.reset_ants()
        for ant in self.anthill.ants:
            ant.path.append(self.graph.start)
            prev_vertex = curr_vertex = self.graph.start
            while True:
                curr_vertex, prev_vertex = self.pick_vertex(self.graph.vertices[curr_vertex],
                                                            self.graph.vertices[prev_vertex])
                if curr_vertex is None:
                    ant.has_found = False
                    break
                ant.path.append(curr_vertex)
                ant.distance_traveled += self.graph.vertices[prev_vertex].neighbours[curr_vertex]["weight"]
                if curr_vertex == self.graph.end:
                    ant.has_found = True
                    break

    def pick_vertex(self, vertex: Vertex, prev_vert: Vertex):
        tau = [[k, ((1 / v["weight"]) ** self.beta_param) * (v["pheromone"] ** self.alpha_param)] for k, v in
               vertex.neighbours.items() if k != prev_vert.id]
        if not len(tau):
            if vertex.id != prev_vert.id:
                return prev_vert.id, vertex.id
            else:
                return None, None
        total = 0
        for val in tau:
            total += val[1]
        if total == 0.0:
            tau = [[k, (1 / v["weight"])] for k, v in vertex.neighbours.items() if k != prev_vert.id]
            for val in tau:
                total += val[1]
        for i in range(len(tau)):
            tau[i][1] /= total
        curr = 1.0
        i = 0
        rand_number = uniform(0, 1)
        while i < len(tau) - 1:
            curr -= tau[i][1]
            if rand_number >= curr:
                break
            i += 1
        return tau[i][0], vertex.id

    def single_pheromone_update(self, ant):
        if ant.has_found:
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

