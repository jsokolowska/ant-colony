"""
    Created by: Rafal Uzarowicz
    Date of creation: 30.03.2020
    Github: https://github.com/RafalUzarowicz
"""

from src.graph import Graph
from src.vertex import Vertex
from sys import maxsize
from src.graph_input import read_graph_txt


def dijkstra(graph: Graph, start_point: Vertex, end_point: Vertex) -> []:
    vertices_to_check = [[v, maxsize, None] for v in graph.vertices.values() if v != start_point]
    vertices_to_check = [[start_point, 0, None]] + vertices_to_check
    vertices_checked = []
    name_to_index = {vertices_to_check[i][0].id: i for i in range(len(vertices_to_check))}
    while len(vertices_to_check) > 0:
        current_vertex = vertices_to_check[0]
        vertices_to_check = vertices_to_check[1:]
        name_to_index[current_vertex[0].id] = -1
        vertices_checked.append(current_vertex)
        for i in range(len(vertices_to_check)):
            name_to_index[vertices_to_check[i][0].id] -= 1
        for neigh in current_vertex[0].neighbours:
            if name_to_index[neigh] < 0:
                continue
            if vertices_to_check[name_to_index[neigh]][1] > current_vertex[1] + \
                    current_vertex[0].neighbours[neigh]:
                vertices_to_check[name_to_index[neigh]][1] = current_vertex[1] + \
                                                             current_vertex[0].neighbours[neigh]
                vertices_to_check[name_to_index[neigh]][2] = current_vertex[0].id
                for i in range(len(vertices_to_check)):
                    if name_to_index[neigh] == i:
                        break
                    if vertices_to_check[i][1] >= vertices_to_check[name_to_index[neigh]][1]:
                        for j in range(i, name_to_index[neigh]):
                            name_to_index[vertices_to_check[j][0].id] += 1
                        vertices_to_check.insert(i, vertices_to_check.pop(name_to_index[neigh]))
                        name_to_index[neigh] = i
                        break
    name_to_index = {vertices_checked[i][0].id: i for i in range(len(vertices_checked))}
    curr_vertex = vertices_checked[name_to_index[end_point.id]]
    path = []
    while True:
        if curr_vertex[2] is None:
            path = [start_point.id] + path
            break
        path = [curr_vertex[0].id] + path
        curr_vertex = vertices_checked[name_to_index[curr_vertex[2]]]
    return path


# g = read_graph_txt()
# p = dijkstra(g, g.vertices[g.start], g.vertices[g.end])
# print(p)
