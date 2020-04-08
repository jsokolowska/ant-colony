"""
    Created by: Rafal Uzarowicz
    Date of creation: 30.03.2020
    Github: https://github.com/RafalUzarowicz
"""

from src.graph import Graph
from src.vertex import Vertex
from sys import maxsize


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
    distance = 0
    while True:
        if curr_vertex[2] is None:
            path = [start_point] + path
            break
        path = [curr_vertex[0].id] + path
        curr_vertex = vertices_checked[name_to_index[curr_vertex[2]]]
    for i in range(len(path)-1):
        prev_vertex = path[i]
        next_vertex = path[i + 1]
        distance += graph.vertices[prev_vertex].neighbours[next_vertex]["weight"]
    return path, distance


def brute_force(graph: Graph) -> ([], int):
    if type(graph.start) is not Vertex or type(graph.end) is not Vertex:
        raise TypeError('Graph start and end id\'s are not of class Vertex')
    else:
        paths = bf_recursion(graph, [], graph.start.id, 0, [])
        return choose_shortest_path(paths)


def bf_recursion(graph: Graph, visited: [], current_id, length, paths: []) -> []:
    if current_id == graph.end.id:
        visited.append(current_id)
        paths.append((visited, length))
    else:
        visited.append(current_id)
        for node in graph.vertices[current_id].neighbours:
            if node not in visited:
                length_copy = update_path_length(graph, current_id, node, length)
                bf_recursion(graph, visited[:], node, length_copy, paths)
    return paths


def update_path_length(graph: Graph, vertex1_id, vertex2_id, length):
    return length + graph.vertices[vertex1_id].neighbours[vertex2_id]["weight"]


def choose_shortest_path(paths) -> ([], int):
    if len(paths) == 0:
        return None
    shortest = paths[0]
    for path in paths:
        if path[1] < shortest[1]:
            shortest = path
    return shortest
