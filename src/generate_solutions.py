"""
    Created by: Rafal Uzarowicz
    Date of creation: 31.03.2020
    Github: https://github.com/RafalUzarowicz
"""
from src.anthill import Anthill
from src.graph import Graph
from src.vertex import Vertex
from random import uniform
from src.graph_input import read_graph_from_file


def pick_vertex(neighbours: {}):
    alpha = 1
    beta = 1
    tau = [[k, (v["weight"] ** beta) * (v["pheromone"] ** alpha)] for k, v in neighbours.items()]
    total = 0
    for val in tau:
        total += val[1]
    for i in range(len(tau)):
        tau[i][1] /= total
    probability = []
    curr = 1.0
    for i in range(len(tau) - 1):
        curr -= tau[i][1]
        probability.append(curr)
    probability.append(0.0)
    rand_number = uniform(0, 1)
    i = 0
    while i < len(probability):
        if rand_number >= probability[i]:
            break
        i += 1
    return tau[i][0]


def generate_solutions(anthill: Anthill, graph: Graph) -> Anthill:
    vertex_lst = list(graph.vertices.keys())
    vertex_lst.remove(graph.start)
    for ant in anthill:
        ant.path.append(graph.start)
        unvisited_vertex_lst = vertex_lst.copy()
        curr_vertex = graph.vertices[graph.start]
        while True:
            prev_vertex = curr_vertex
            available_vertices = {k: v for k, v in curr_vertex.neighbours.items() if k in unvisited_vertex_lst}
            if not len(available_vertices):
                break
            chosen_vertex = pick_vertex(available_vertices)
            unvisited_vertex_lst.remove(chosen_vertex)
            curr_vertex = graph.vertices[chosen_vertex]
            ant.path.append(curr_vertex.id)
            ant.distance_traveled += prev_vertex.neighbours[chosen_vertex]["weight"]
            if curr_vertex.id == graph.end:
                ant.has_found = True
                break
    string = ""
    for ant in anthill:
        if ant.has_found:
            string += "1"
        else:
            string += "0"
    print(string)
    return anthill


anth = Anthill(100)
g = read_graph_from_file("../graph_example.txt")
generate_solutions(anth, g)

pick_vertex(g.vertices[g.start].neighbours)
