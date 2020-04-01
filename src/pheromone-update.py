"""
    Created by: Rafal Uzarowicz
    Date of creation: 01.04.2020
    Github: https://github.com/RafalUzarowicz
"""
from src.anthill import Anthill
from src.graph import Graph
from src.vertex import Vertex
from random import uniform
from src.graph_input import read_graph_from_file

def pheromone_update( anthill: Anthill, graph: Graph ):
    q_param = 1
    edge_counter = { k:v for k, v in graph.vertices }