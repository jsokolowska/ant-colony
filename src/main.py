# import argparse
#
#
# parser = argparse.ArgumentParser(description="Ant Colony Optimization for finding a path in weighted graph")
# parser.add_argument('filename')
from src.ant_colony_optimization import AntColonyOptimization
from src.generate_input import generate_input, generate_with_bridges
from src.graph_input import read_graph_txt
from src.path_search_algo import dijkstra

# generate_input(100, 0.1, 30)
generate_with_bridges(200, 0.5, 15)
graph = read_graph_txt(keyword_1="auto", keyword_2="20")
# our_graph = read_graph_txt(keyword_1="graph", keyword_2="example")
dijk = dijkstra(graph, graph.start, graph.end)
# aco = AntColonyOptimization(ants_num=30, graph=graph)
# result = aco.run(40)
# print("Result: " + str(result))
print("Dijkstra: " + str(dijk))
