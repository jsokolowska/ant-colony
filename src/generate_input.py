"""
    Created by: Joanna Sokołowska
    Date of creation: 30.03.2020
    Date of last modification: 14.04.2020
    Github: https://github.com/jsokolowska
"""

from random import uniform
from random import randrange


def generate_input(vertex_num, probability, file_name="graph_example_auto.txt"):  # currently handling up ro 23 vertices
    if vertex_num < 2 or probability < 0 or probability > 1:
        raise ValueError('Probability should be between 0 and 1, while vertex_num must be at least 2')
    all_vertices = [chr(i) for i in range(ord('a'), ord('a') + vertex_num)]
    all_edges = [(all_vertices[a], all_vertices[b]) for a in range(vertex_num) for b in range(a + 1, vertex_num)]

    chosen_edges = set()
    for edge in all_edges:
        rand_num = uniform(0, 1)
        if rand_num < probability:
            chosen_edges.add(edge)

    lines = []
    for edge in chosen_edges:
        weight = randrange(1, 20)
        lines.append(" ".join([edge[0], edge[1], str(weight)]))

    PATH = "../graphs/"
    file_name = PATH + file_name
    with open(file_name, 'w') as file:
        start_vertex = chr(ord('a') + randrange(0, vertex_num - 1))
        end_vertex = chr(ord('a') + randrange(0, vertex_num - 1))
        lines.append(" ".join([start_vertex, end_vertex]))
        file.write("\n".join(lines))
