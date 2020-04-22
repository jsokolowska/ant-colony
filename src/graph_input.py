"""
    Created by: Rafal Uzarowicz
    Date of creation: 27.03.2020
    Github: https://github.com/RafalUzarowicz
"""

from src.graph import Graph
from pathlib import Path
import random


def read_graph(file_name: str):
    path = "../graphs/"
    return read_graph_from_file(path + file_name)


def read_graph_from_file(file_name: str):
    try:
        with open(file_name) as graph_file:
            graph_temp = Graph()
            for line in graph_file.readlines():
                lst = line.split()
                if len(lst) == 2:
                    if graph_temp.is_vertex(lst[0]):
                        graph_temp.start = lst[0]
                    if graph_temp.is_vertex(lst[1]):
                        graph_temp.end = lst[1]
                elif len(lst) == 3:
                    vertex_1 = lst[0]
                    vertex_2 = lst[1]
                    edge_weight = int(lst[2])
                    if edge_weight > 0:
                        graph_temp.add_edge(vertex_1.strip(), vertex_2.strip(), edge_weight)
                else:
                    print("ERROR: Wrong file format.")
                    return Graph()
            if graph_temp.start is None:
                graph_temp.start = graph_temp.vertices[list(graph_temp.vertices.keys())[0]]
            if graph_temp.end is None:
                graph_temp.end = graph_temp.vertices[list(graph_temp.vertices.keys())[-1]]
            return graph_temp
    except FileNotFoundError:
        print("ERROR: File ", file_name, " not found.")
        return None


def read_graph_txt(which_file="first", keyword_1="graph", keyword_2="example"):
    data_folder = Path("../")
    list_of_txt = [x for x in data_folder.rglob('*.txt') if x.is_file()]
    if which_file == "first":
        for file in list_of_txt:
            if file.name.find(keyword_1) >= 0 and file.name.find(keyword_2) >= 0:
                graph_file = str(file.parent) + "/" + file.name
                return read_graph_from_file(graph_file)
    elif which_file == "random":
        file_lst = []
        for file in list_of_txt:
            if file.name.find(keyword_1) >= 0 and file.name.find(keyword_2) >= 0:
                file_lst.append(str(file.parent) + "/" + file.name)
        return read_graph_from_file(file_lst[random.randint(0, len(file_lst) - 1)])
    else:
        print("ERROR: Wrong read mode.")
