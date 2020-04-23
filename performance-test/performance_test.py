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
from src.generate_input import generate_input, generate_input_to_txt, generate_with_bridges
from documentation.remove_auto_graphs import remove_auto_graphs
import time
# import matplotlib.pyplot as plt
#
# x = [1, 2, 3, 4, 5]
# y = [11, 7, 4, 5, 6]
# plt.plot(x, y, "r--")
# plt.show()

# remove_auto_graphs()
name = generate_input(100, 0.05)
# name = generate_with_bridges(100, 0.1, 10)
# name = "auto_graph_100_0.0063.txt"
# name = "auto_graph_100_0.05.txt"
graph = read_graph(name)
aco = AntColonyOptimization(graph=graph, ants_num=100, ls_flag=True)
start_time = time.time()
print(time.ctime())
result = aco.run(1000)
print("aco: ", result[1], result[0])
print("--- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
d_res = dijkstra(graph, graph.start, graph.end)
print("dijkstra: ", d_res[1], d_res[0])
print("--- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
bf_res = brute_force(graph)
print("bf: ", bf_res[1], bf_res[0])
print("--- %s seconds ---" % (time.time() - start_time))

iterations_per_test = 20
iterations_per_graph_size = 3
graph_density = 0.1
graph_sizes = [10, 20, 30]
ants_numbers = [5, 10, 50, 100]
ants_iterations = [10, 50, 100]

# for graph_size in range(25, 50):
#     print(graph_size)
#     for i in range(iterations_per_graph_size):
#         graph = read_graph(generate_input(graph_size, graph_density))
#         print(graph)
#         start_time = time.time()
#         bf_res = brute_force(graph)
#         print("bf: ", bf_res)
#         print("--- %s seconds ---" % (time.time() - start_time))
#
# remove_auto_graphs()
