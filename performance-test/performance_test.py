"""
    Created by: Rafal Uzarowicz
    Date of creation: 22.04.2020
    Github: https://github.com/RafalUzarowicz
"""
from matplotlib.font_manager import FontProperties

from src.graph import Graph
from src.graph_input import read_graph_from_file, read_graph
from src.path_search_algo import dijkstra
from src.path_search_algo import brute_force
from src.ant_colony_optimization import AntColonyOptimization
from src.generate_input import generate_input, generate_input_to_txt, generate_with_bridges
from documentation.remove_auto_graphs import remove_auto_graphs
import time
import matplotlib.pyplot as plt


def test_plot_time_graph_size():
    iterations_per_test = 20
    iterations_per_graph_size = 10
    graph_density = 0.2
    graph_sizes = [20, 101, 5]

    results = {}

    for graph_size in range(graph_sizes[0], graph_sizes[1], graph_sizes[2]):
        results[graph_size] = {}
        for i in range(iterations_per_graph_size):
            name = generate_input(graph_size, graph_density)
            # name = generate_with_bridges(graph_size, graph_density, 8)
            graph = read_graph(name)
            results[graph_size][i] = {}
            for ants_number in [graph_size // 2, graph_size, graph_size * 2]:
                results[graph_size][i][ants_number] = {}
                for j in range(iterations_per_test):
                    aco = AntColonyOptimization(graph=graph, ants_num=ants_number, ls_flag=True)
                    start_time = time.time()
                    result = aco.run(1000)
                    end_time = time.time() - start_time
                    # end_time = time.time()
                    # print("--- %s seconds ---" % end_time)
                    results[graph_size][i][ants_number][j] = end_time
                    # print("Results:", " graph_size= ", graph_size, ", ants_number= ", ants_number, " : ",
                    #       results[graph_size][i][ants_number][j])

    final_results = {}
    for graph_size in range(graph_sizes[0], graph_sizes[1], graph_sizes[2]):
        final_results[graph_size] = {}
        tmp_results = {}
        counter = {}
        for i in range(iterations_per_graph_size):
            for ants_number in results[graph_size][i]:
                total = 0.0
                for j in range(iterations_per_test):
                    total += results[graph_size][i][ants_number][j]
                results[graph_size][i][ants_number] = total / len(results[graph_size][i][ants_number])
                if tmp_results.get(ants_number, None) is None:
                    tmp_results[ants_number] = results[graph_size][i][ants_number]
                    counter[ants_number] = 1
                else:
                    tmp_results[ants_number] += results[graph_size][i][ants_number]
                    counter[ants_number] += 1
        for k in tmp_results.keys():
            final_results[graph_size][k] = tmp_results[k] / counter[k]

    # for graph_size in range(graph_sizes[0], graph_sizes[1], graph_sizes[2]):
    #     for ants_number in final_results[graph_size]:
    #         print("Results:", " graph_size= ", graph_size, ", ants_number= ", ants_number, " : ",
    #               final_results[graph_size][ants_number])

    x = list(final_results.keys())
    y = [[], [], []]
    for graph_size in final_results.keys():
        y[0].append(final_results[graph_size][graph_size // 2])
        y[1].append(final_results[graph_size][graph_size])
        y[2].append(final_results[graph_size][graph_size * 2])
    plt.plot(x, y[0], "bo:", label="ants_num=graph_size//2")
    plt.plot(x, y[1], "ro:", label="ants_num=graph_size")
    plt.plot(x, y[2], "go:", label="ants_num=graph_size*2")
    plt.xlabel("liczba wierzcholkow")
    plt.xticks(x, x)
    plt.ylabel("czas wykonywania")
    plt.legend(loc='best', shadow=True, fontsize='small')
    plt.title("Sredni czas wykonywania w zaleznosci od rozmiaru grafu.")
    plt.show()

    remove_auto_graphs()

def test_plot_diff_ants():
    iterations_per_test = 20
    iterations_per_ants_number = 10
    graph_density = 0.2
    ants_numbers = [20, 101, 5]

    remove_auto_graphs()

    results = {}

    for ant_number in range(ants_numbers[0], ants_numbers[1], ants_numbers[2]):
        results[ant_number] = {}
        for i in range(iterations_per_ants_number):
            results[ant_number][i] = {}
            for g_size in [ant_number * 2, ant_number * 3, ant_number * 4]:
                name = generate_input(g_size, graph_density)
                # name = generate_with_bridges(g_size, graph_density, 8)
                graph = read_graph(name)
                d_res = dijkstra(graph, graph.start, graph.end)
                results[ant_number][i][g_size] = {}
                for j in range(iterations_per_test):
                    aco = AntColonyOptimization(graph=graph, ants_num=ant_number, ls_flag=True)
                    result = aco.run(1000)
                    results[ant_number][i][g_size][j] = result[1] / d_res[1]

    final_results = {}
    for ant_number in range(ants_numbers[0], ants_numbers[1], ants_numbers[2]):
        final_results[ant_number] = {}
        tmp_results = {}
        counter = {}
        for i in range(iterations_per_ants_number):
            for g_size in results[ant_number][i]:
                total = 0.0
                for j in range(iterations_per_test):
                    total += results[ant_number][i][g_size][j]
                results[ant_number][i][g_size] = total / len(results[ant_number][i][g_size])
                if tmp_results.get(g_size, None) is None:
                    tmp_results[g_size] = results[ant_number][i][g_size]
                    counter[g_size] = 1
                else:
                    tmp_results[g_size] += results[ant_number][i][g_size]
                    counter[g_size] += 1
        for k in tmp_results.keys():
            final_results[ant_number][k] = tmp_results[k] / counter[k]

    # for ant_number in range(ants_numbers[0], ants_numbers[1], ants_numbers[2]):
    #     for g_size in final_results[ant_number]:
    #         print("Results:", " graph_size= ", g_size, ", ants_number= ", ant_number, " : ",
    #               final_results[ant_number][g_size])

    x = list(final_results.keys())
    # y = [[], [], []]
    y = []
    for ant_number in final_results.keys():
        # y[0].append(final_results[ant_number][ant_number * 2])
        # y[1].append(final_results[ant_number][ant_number * 3])
        # y[2].append(final_results[ant_number][ant_number * 4])
        y.append((final_results[ant_number][ant_number * 2]+final_results[ant_number][ant_number * 3]+final_results[ant_number][ant_number * 4])/3)
    # plt.plot(x, y[0], "bo:", label="graph_size=ants_number*2")
    # plt.plot(x, y[1], "ro:", label="graph_size=ants_number*3")
    # plt.plot(x, y[2], "go:", label="graph_size=ants_number*4")
    plt.plot(x, y, "go:")
    plt.xlabel("liczba mrowek")
    plt.xticks(x, x)
    plt.ylabel("stosunek dlugosci znalezionej drogi do najkrotszej drogi")
    plt.legend(loc='best', shadow=True, fontsize='small')
    plt.title("Sredni stosunek dlugosci znalezionej drogi do najkrotszej drogi w zaleznosci od rozmiaru mrowiska.")
    plt.show()

    remove_auto_graphs()

# x = [1, 2, 3, 4, 5]
# y = [11, 7, 4, 5, 6]
# # plt.plot(x, y, "ro--")
# x = [1, 2, 3, 4, 5]
# z = [12, 8, 5, 6, 7]
# w = [x, y, z]
# plt.plot(w[0], w[1:], "bo:")
# plt.show()

# remove_auto_graphs()
# name = generate_input(100, 0.05)
# name = generate_with_bridges(500, 0.3, 5)
# name = "auto_graph_100_0.0063.txt"
# name = "auto_graph_100_0.05.txt"
# name = "auto_graph_100_0.1000.txt"
# graph = read_graph(name)
# aco = AntColonyOptimization(graph=graph, ants_num=1, ls_flag=True)
# start_time = time.time()
# print(time.ctime())
# result = aco.run(1000)
# print("aco: ", result[1], result[0])
# print("--- %s seconds ---" % (time.time() - start_time))
# start_time = time.time()
# d_res = dijkstra(graph, graph.start, graph.end)
# print("dijkstra: ", d_res[1], d_res[0])
# print("--- %s seconds ---" % (time.time() - start_time))
# start_time = time.time()
# bf_res = brute_force(graph)
# print("bf: ", bf_res[1], bf_res[0])
# print("--- %s seconds ---" % (time.time() - start_time))

