"""
    Created by: Rafal Uzarowicz
    Date of creation: 31.03.2020
    Github: https://github.com/RafalUzarowicz
"""
from src.anthill import Anthill
from src.graph import Graph
from src.vertex import Vertex
from random import uniform


def pick_vertex(vertex: Vertex, prev_vertex: Vertex):
    alpha_param = 1
    beta_param = 1
    tau = [[k, ((1 / v["weight"]) ** beta_param) * (v["pheromone"] ** alpha_param)] for k, v in
           vertex.neighbours.items() if k != prev_vertex.id]
    if not len(tau):
        if vertex.id != prev_vertex.id:
            return prev_vertex.id, vertex.id
        else:
            return None, None
    total = 0
    for val in tau:
        total += val[1]
    if total == 0.0:
        tau = [[k, (1 / v["weight"])] for k, v in vertex.neighbours.items() if k != prev_vertex.id]
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


def generate_solutions(anthill: Anthill, graph: Graph) -> Anthill:
    anthill.reset_ants()
    for ant in anthill:
        ant.path.append(graph.start)
        prev_vertex = curr_vertex = graph.start
        while True:
            curr_vertex, prev_vertex = pick_vertex(graph.vertices[curr_vertex], graph.vertices[prev_vertex])
            if curr_vertex is None:
                ant.has_found = False
                break
                break
            ant.path.append(curr_vertex)
            ant.distance_traveled += graph.vertices[prev_vertex].neighbours[curr_vertex]["weight"]
            if curr_vertex == graph.end:
                ant.has_found = True
                break
    for ant in anthill:
        print(ant.has_found, "\t", ant.distance_traveled, "\t", ant.path)
    return anthill
