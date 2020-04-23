"""
    Created by: Rafal Uzarowicz
    Date of creation: 22.04.2020
    Github: https://github.com/RafalUzarowicz
"""

from src.graph import Graph
from src.graph_input import read_graph_from_file, read_graph
from src.path_search_algo import dijkstra
from src.path_search_algo import brute_force
from src.ant_colony_optimization import AntColonyOptimization
from src.generate_input import generate_input, generate_input_to_txt
from documentation.remove_auto_graphs import remove_auto_graphs
import time

# name = generate_input(15, 0.5)
# name = "auto_graph_15_0.5.txt"
# graph = read_graph(name)
# aco = AntColonyOptimization(graph=graph, ants_num=100, ls_flag=False)
# start_time = time.time()
# print(time.ctime())
# result = aco.run(100)
# print("aco: ", result[0], result[1])
# print("--- %s seconds ---" % (time.time() - start_time))
# start_time = time.time()
# d_res = dijkstra(graph, graph.start, graph.end)
# print("dijkstra: ", d_res)
# print("--- %s seconds ---" % (time.time() - start_time))
# start_time = time.time()
# bf_res = brute_force(graph)
# print("bf: ", bf_res)
# print("--- %s seconds ---" % (time.time() - start_time))

iterations_per_test = 20
iterations_per_graph_size = 3
graph_density = 0.1
graph_sizes = [10, 20, 30]
ants_numbers = [5, 10, 50, 100]
ants_iterations = [10, 50, 100]

for graph_size in range(25, 50):
    print(graph_size)
    for i in range(iterations_per_graph_size):
        graph = read_graph(generate_input(graph_size, graph_density))
        print(graph)
        start_time = time.time()
        bf_res = brute_force(graph)
        print("bf: ", bf_res)
        print("--- %s seconds ---" % (time.time() - start_time))

remove_auto_graphs()
