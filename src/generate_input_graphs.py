"""
    Created by: Joanna Sokołowska
    Date of creation: 30.03.2020
    Date of last modification: 02.04.2020
    Github: https://github.com/jsokolowska
"""

import random


def generate_input(vertex_num, density, file_name="graph_example_auto.txt"):
    if vertex_num < 2 or density < 0 or density > 1:
        raise ValueError('Density should be between 0 and 1, while vertex_num must be at least 2')

    max_edges = vertex_num * (vertex_num - 1) / 2
    expected_edges = density * max_edges
    edges = min(max(expected_edges, vertex_num), max_edges)
    lone_vertices = {chr(a) for a in range(ord('a'), ord('a') + vertex_num)}
    created_edges = set()

    for a in range(ord('a'), ord('a') + vertex_num):
        start_vertex = chr(a)
        if start_vertex in lone_vertices:
            lone_vertices.remove(start_vertex)
            end_vertex = chr(ord('a') + random.randrange(0, vertex_num - 2))
            if end_vertex >= start_vertex:
                end_vertex = chr(ord(end_vertex) + 1)
            new_edge = (start_vertex, end_vertex)
            if new_edge not in created_edges:
                created_edges.add((start_vertex, end_vertex))
                if end_vertex in lone_vertices:
                    lone_vertices.remove(end_vertex)
                edges -= 1

    while edges > 0:
        start_vertex = chr(ord('a') + random.randrange(0, vertex_num - 1))
        end_vertex = chr(ord('a') + random.randrange(0, vertex_num - 1))
        if end_vertex >= start_vertex:
            end_vertex = chr(ord(end_vertex) + 1)
        new_edge = (start_vertex, end_vertex)
        if new_edge not in created_edges:
            created_edges.add(new_edge)
            edges -= 1

    lines = []
    for edge in created_edges:
        edge_weight = str(random.randrange(1, 20))
        line = " ".join([edge[0], edge[1], edge_weight])
        lines.append(line)

    PATH = "../graphs/"
    file_name = PATH + file_name
    with open(file_name, 'w') as file:
        start_vertex = chr(ord('a') + random.randrange(0, vertex_num - 1))
        end_vertex = chr(ord('a') + random.randrange(0, vertex_num - 1))
        lines.append(" ".join([start_vertex, end_vertex]))
        file.write("\n".join(lines))

