"""
    Created by: Rafal Uzarowicz
    Date of creation: 30.03.2020
    Github: https://github.com/RafalUzarowicz
"""

from src.graph import Graph
from src.vertex import Vertex
from sys import maxsize
from src.graph_input import read_graph_txt


def dijkstra(graph: Graph, start_point, end_point) -> []:
    if type(start_point) is Vertex and type(end_point) is Vertex:
        start_point = start_point.id
        end_point = end_point.id
    elif type(start_point) is str and type(end_point) is str:
        pass
    else:
        print("ERROR: Wrong argument type.")
        raise TypeError
    if start_point not in graph.vertices or end_point not in graph.vertices:
        print("ERROR: Point not found in graph.")
        raise ValueError
    vertices_to_check = [[v, maxsize, None] for v in graph.vertices.values() if v.id != start_point]
    vertices_to_check = [[graph.vertices[start_point], 0, None]] + vertices_to_check
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
                    current_vertex[0].neighbours[neigh]["weight"]:
                vertices_to_check[name_to_index[neigh]][1] = current_vertex[1] + \
                                                             current_vertex[0].neighbours[neigh]["weight"]
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
    curr_vertex = vertices_checked[name_to_index[end_point]]
    path = []
    while True:
        if curr_vertex[2] is None:
            path = [start_point] + path
            break
        path = [curr_vertex[0].id] + path
        curr_vertex = vertices_checked[name_to_index[curr_vertex[2]]]
    return path


g = read_graph_txt()
p = dijkstra(g, g.vertices[g.start], g.vertices[g.end])
print(p)
