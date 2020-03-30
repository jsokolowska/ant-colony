"""
    Created by: Rafal Uzarowicz
    Date of creation: 27.03.2020
    Github: https://github.com/RafalUzarowicz
"""

from src.graph import Graph
from pathlib import Path
import random


def read_graph_from_file(fileName: str) -> Graph:
    try:
        with open(fileName) as graph_file:
            graph_temp = Graph()
            for line in graph_file.readlines():
                lst = line.split()
                if len(lst) == 2:
                    start = lst[0]
                    if graph_temp.is_vertex(start):
                        graph_temp.start = start
                    end = lst[1]
                    if graph_temp.is_vertex(end):
                        graph_temp.end = end
                elif len(lst) > 2:
                    vertex_1 = lst[0]
                    vertex_2 = lst[1]
                    edge_weight = int(lst[2])
                    if edge_weight > 0:
                        graph_temp.add_edge(vertex_1.strip(), vertex_2.strip(), edge_weight)
            return graph_temp
    except FileNotFoundError:
        print("ERROR: File ", fileName, " not found.")


def read_graph_txt(which_file="first") -> Graph:
    data_folder = Path("./")
    list_of_txt = [x for x in data_folder.rglob('../*.txt') if x.is_file()]
    if which_file == "first":
        for file in list_of_txt:
            if file.name.find("graph") >= 0 and file.name.find("example") >= 0:
                graph_file = str(file.parent) + "/" + file.name
                return read_graph_from_file(graph_file)
    elif which_file == "random":
        file_lst = []
        for file in list_of_txt:
            if file.name.find("graph") >= 0 and file.name.find("example") >= 0:
                file_lst.append(str(file.parent) + "/" + file.name)
        return read_graph_from_file(file_lst[random.randint(0, len(file_lst) - 1)])
    else:
        print("ERROR: Wrong read mode.")

# graph = read_graph_txt("random")
# print(str(graph))
