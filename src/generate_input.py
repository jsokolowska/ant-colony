"""
    Created by: Joanna Sokołowska
    Date of creation: 30.03.2020
    Date of last modification: 14.04.2020
    Github: https://github.com/jsokolowska
"""

from random import uniform
from random import randrange


def generate_input(vertex_num, probability, max_weight=20):
    file_name = "auto_graph_" + str(vertex_num) + "_" + str(probability) + ".txt"
    generate_input_to_txt(vertex_num, probability, file_name, max_weight)


def generate_input_to_txt(vertex_num, probability, file_name, max_weight=20):
    if vertex_num < 2 or probability < 0 or probability > 1:
        raise ValueError('Probability should be between 0 and 1, while vertex_num must be at least 2')
    if max_weight < 1:
        raise ValueError("Argument max_weight must be at least 1.")

    # generate vertices id's
    all_vertices = []
    max_letter_index = ord('z') - ord('a') + 1
    i = 0
    j = 0
    while j < max_letter_index and i < vertex_num:
        all_vertices.append(chr(ord("a") + j))
        j += 1
        i += 1

    for k in range(vertex_num // max_letter_index):
        j = 0
        while j < max_letter_index and i < vertex_num:
            all_vertices.append(all_vertices[k] + chr(ord("a") + j))
            j += 1
            i += 1

    # all_vertices = [chr(i) for i in range(ord('a'), ord('a') + vertex_num)]
    # generate all possible paths
    all_vertices = sorted(all_vertices)
    all_edges = [(all_vertices[a], all_vertices[b]) for a in range(vertex_num) for b in range(a + 1, vertex_num)]
    # choose end vertices
    start_vertex = all_vertices[randrange(0, vertex_num - 1)]
    all_vertices.remove(start_vertex)
    end_vertex = all_vertices[randrange(0, vertex_num - 2)]

    chosen_edges = set()
    max_edges_num = len(all_edges)
    # guarantee path:
    used_edges = 0
    path = []
    curr_vertex = start_vertex

    while curr_vertex != end_vertex:
        path.append(curr_vertex)
        next_vertex = all_vertices[randrange(0, len(all_vertices))]
        edge = (next_vertex, curr_vertex)
        if curr_vertex < next_vertex:
            edge = (curr_vertex, next_vertex)
        all_vertices.remove(next_vertex)
        chosen_edges.add(edge)
        all_edges.remove(edge)
        # try:
        #     all_edges.remove(edge)
        # except ValueError:
        #     try:
        #         print("Tried to remove edge: " + str(edge))
        #         edge = (next_vertex, curr_vertex)
        #         all_edges.remove(edge)
        #     except ValueError:
        #         print("Tried to remove edge: " + curr_vertex + ", " + next_vertex)
        #         with open("all_edges.txt", "a") as file:
        #             file.write(str(edge) + "\n\n" + str(all_edges) + "\n\n")

        used_edges += 1
        curr_vertex = next_vertex

    if max_edges_num * probability > used_edges:
        # adjust probability value to take into account used edges
        probability = (probability * max_edges_num - used_edges) / (max_edges_num - used_edges)
        for edge in all_edges:
            rand_num = uniform(0, 1)
            if rand_num < probability:
                chosen_edges.add(edge)

    lines = []
    for edge in chosen_edges:
        weight = randrange(1, max_weight + 1)
        lines.append(" ".join([edge[0], edge[1], str(weight)]))

    path = "graphs/"
    file_name = path + file_name
    with open(file_name, 'w') as file:
        # start_vertex = all_vertices[randrange(0, vertex_num - 1)]
        # # start_vertex = chr(ord('a') + randrange(0, vertex_num - 1))
        # end_vertex = all_vertices[randrange(0, vertex_num - 1)]
        # # end_vertex = chr(ord('a') + randrange(0, vertex_num - 1))
        lines.append(" ".join([start_vertex, end_vertex]))
        file.write("\n".join(lines))


def generate_with_bridges(vertex_num, probability, bridges_num, max_weight=20):
    if vertex_num < 2 or probability < 0 or probability > 1 or bridges_num<1:
        raise ValueError('Probability should be between 0 and 1, bridges_num greater than 1 while vertex_num must be at least 2')
    if max_weight < 1:
        raise ValueError("Argument max_weight must be at least 1.")
    if vertex_num < bridges_num*2:
        raise ValueError("Not enough vertices for that many bridges")
    # generate vertices id's
    all_vertices = []
    max_letter_index = ord('z') - ord('a') + 1
    i = 0
    j = 0
    while j < max_letter_index and i < vertex_num:
        all_vertices.append(chr(ord("a") + j))
        j += 1
        i += 1

    for k in range(vertex_num // max_letter_index):
        j = 0
        while j < max_letter_index and i < vertex_num:
            all_vertices.append(all_vertices[k] + chr(ord("a") + j))
            j += 1
            i += 1

    all_vertices = sorted(all_vertices)
    # all_edges = [(all_vertices[a], all_vertices[b]) for a in range(vertex_num) for b in range(a + 1, vertex_num)]
    groups = []
    for bridge in range(bridges_num):
        groups.append([])

    # divide into as many groups as there are bridges
    # for vertex in all_vertices:
    #     groups[randrange(0, bridges_num)].append(vertex)

    gr_size = vertex_num//bridges_num
    for i in range(bridges_num-1):
        groups[i] = all_vertices[i*gr_size:(i+1)*gr_size]

    groups[bridges_num-1] = all_vertices[(bridges_num-1) * gr_size:]

    global_start = groups[0][randrange(0, len(groups[0]))]
    global_end = None

    start_vertex = global_start
    end_vertex = None
    chosen_edges = set()
    bridges_path = [start_vertex]
    for i in range(len(groups)):
        group = groups[i]
        if len(group) == 0:
            print("Empty group " + str(i) + " out of " + str(bridges_num))
            continue
        group_edges = [(group[a], group[b]) for a in range(len(group)) for b in range(a+1, len(group))]
        group.remove(start_vertex)
        end_vertex = group[randrange(0, len(group))]
        used_edges = 0
        curr_vertex = start_vertex
        max_edges = len(group_edges)

        # create path between them
        while curr_vertex != end_vertex:
            next_vertex = group[randrange(0, len(group))]
            edge = (next_vertex, curr_vertex)
            if curr_vertex < next_vertex:
                edge = (curr_vertex, next_vertex)
            group_edges.remove(edge)
            chosen_edges.add(edge)
            group.remove(next_vertex)
            used_edges += 1
            curr_vertex = next_vertex

        bridges_path.append(end_vertex)
        # create other paths in graph
        if max_edges * probability > used_edges:
            # adjust probability value to take into account used edges
            probability = (probability * max_edges - used_edges) / (max_edges - used_edges)
            for edge in group_edges:
                rand_num = uniform(0, 1)
                if rand_num < probability:
                    chosen_edges.add(edge)

        if i != len(groups)-1:
            start_vertex = groups[i+1][randrange(0, len(groups[i+1]))]

    global_end = end_vertex
    # add all bridges:
    if len(bridges_path) > 1:
        for i in range(len(bridges_path)-1):
            bridge = (bridges_path[i], bridges_path[i+1])
            chosen_edges.add(bridge)

    lines = []
    for edge in chosen_edges:
        weight = randrange(1, max_weight + 1)
        lines.append(" ".join([edge[0], edge[1], str(weight)]))

    path = "../graphs/"
    probability_str = "{:.4f}".format(probability)
    file_name = "auto_graph_" + str(vertex_num) + "_" + probability_str + ".txt"
    file_name = path + file_name
    with open(file_name, 'w') as file:
        # start_vertex = all_vertices[randrange(0, vertex_num - 1)]
        # # start_vertex = chr(ord('a') + randrange(0, vertex_num - 1))
        # end_vertex = all_vertices[randrange(0, vertex_num - 1)]
        # # end_vertex = chr(ord('a') + randrange(0, vertex_num - 1))
        lines.append(" ".join([global_start, global_end]))
        file.write("\n".join(lines))
