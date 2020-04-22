"""
    Created by: Rafal Uzarowicz
    Date of creation: 22.04.2020
    Github: https://github.com/RafalUzarowicz
"""

from src.graph import Graph
from src.graph_input import read_graph_from_file
from src.path_search_algo import dijkstra
from src.path_search_algo import brute_force
from src.ant_colony_optimization import AntColonyOptimization
from src.generate_input import generate_input
import time

generate_input(100, 0.5, "graph_performance.txt")
graph = read_graph_from_file("../graphs/graph_performance.txt")
aco = AntColonyOptimization(graph=graph, ants_num=20, ls_flag=False)
start_time = time.time()
result = aco.run(100)
print("aco: ", result[0], result[1])
print("--- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
d_res = dijkstra(graph, graph.start, graph.end)
print("dijkstra: ", d_res)
print("--- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
bf_res = brute_force(graph)
print("bf: ", bf_res)
print("--- %s seconds ---" % (time.time() - start_time))

