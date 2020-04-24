"""
    Created by: Rafal Uzarowicz
    Date of creation: 22.04.2020
    Github: https://github.com/RafalUzarowicz
"""

from src.graph_input import read_graph
from src.path_search_algo import dijkstra
from src.path_search_algo import brute_force
from src.ant_colony_optimization import AntColonyOptimization
from src.generate_input import generate_input
from documentation.remove_auto_graphs import remove_auto_graphs
import time
import matplotlib.pyplot as plt


def test_plot_time_graph_size(iterations_per_test=20, iterations_per_graph_size=10, graph_density=0.2,
                              graph_sizes=(20, 101, 5)):
    results = {}
    for graph_size in range(graph_sizes[0], graph_sizes[1], graph_sizes[2]):
        results[graph_size] = {}
        for i in range(iterations_per_graph_size):
            name = generate_input(graph_size, graph_density)
            graph = read_graph(name)
            results[graph_size][i] = {}
            for ants_number in [graph_size // 2, graph_size, graph_size * 2]:
                results[graph_size][i][ants_number] = {}
                for j in range(iterations_per_test):
                    aco = AntColonyOptimization(graph=graph, ants_num=ants_number, ls_flag=True)
                    start_time = time.time()
                    aco.run(1000)
                    end_time = time.time() - start_time
                    results[graph_size][i][ants_number][j] = end_time

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

    x = list(final_results.keys())
    y = [[], [], []]
    for graph_size in final_results.keys():
        y[0].append(final_results[graph_size][graph_size // 2])
        y[1].append(final_results[graph_size][graph_size])
        y[2].append(final_results[graph_size][graph_size * 2])

    plt.plot(x, y[0], "bo:", label="ants_num=graph_size//2")
    plt.plot(x, y[1], "ro:", label="ants_num=graph_size")
    plt.plot(x, y[2], "go:", label="ants_num=graph_size*2")
    plt.xlabel("Liczba wierzchołków")
    plt.xticks(x, x)
    plt.ylabel("Czas wykonywania [sekundy]")
    plt.legend(loc='best', shadow=True, fontsize='small')
    plt.title("Średni czas wykonywania w zależności od rozmiaru grafu.")
    plt.savefig("test_plot_time_graph_size_" + time.ctime().replace(" ", "_").replace(":", "_") + ".png")
    plt.show()

    remove_auto_graphs()


def test_plot_diff_ants(iterations_per_test=10, iterations_per_ants_number=5, graph_density=0.2,
                        ants_numbers=(20, 101, 5)):
    results = {}
    for ant_number in range(ants_numbers[0], ants_numbers[1], ants_numbers[2]):
        results[ant_number] = {}
        for i in range(iterations_per_ants_number):
            results[ant_number][i] = {}
            for g_size in [ant_number * 2, ant_number * 3, ant_number * 4]:
                name = generate_input(g_size, graph_density)
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

    x = list(final_results.keys())
    y = []
    for ant_number in final_results.keys():
        y.append((final_results[ant_number][ant_number * 2] + final_results[ant_number][ant_number * 3] +
                  final_results[ant_number][ant_number * 4]) / 3)

    plt.plot(x, y, "go:")
    plt.xlabel("Liczba mrówek")
    plt.xticks(x, x)
    plt.ylabel("Stosunek długości znalezionej drogi do najkrótszej drogi")
    plt.legend(loc='best', shadow=True, fontsize='small')
    plt.title("Średni stosunek długości znalezionej drogi do najkrótszej drogi w zależnosci od rozmiaru mrowiska.")
    plt.savefig("test_plot_diff_ants_" + time.ctime().replace(" ", "_").replace(":", "_") + ".png")
    plt.show()

    remove_auto_graphs()


def test_compare_local_search_on_off(iterations_per_test=10, iterations_per_graph_size=5, graph_density=0.2,
                                     graph_sizes=(20, 101, 5)):
    daemon_actions = ["local_search", "pheromone_update"]

    results = {}
    for daemon in daemon_actions:
        results[daemon] = {}
        if daemon == "local_search":
            ls_flag = True
        else:
            ls_flag = False
        for graph_size in range(graph_sizes[0], graph_sizes[1], graph_sizes[2]):
            results[daemon][graph_size] = {}
            for i in range(iterations_per_graph_size):
                name = generate_input(graph_size, graph_density)
                graph = read_graph(name)
                results[daemon][graph_size][i] = {}
                for ants_number in [graph_size // 2, graph_size, graph_size * 2]:
                    results[daemon][graph_size][i][ants_number] = {}
                    for j in range(iterations_per_test):
                        aco = AntColonyOptimization(graph=graph, ants_num=ants_number, ls_flag=ls_flag)
                        start_time = time.time()
                        aco.run(1000)
                        end_time = time.time() - start_time
                        results[daemon][graph_size][i][ants_number][j] = end_time

    final_results = {}
    for daemon in daemon_actions:
        final_results[daemon] = {}
        for graph_size in range(graph_sizes[0], graph_sizes[1], graph_sizes[2]):
            final_results[daemon][graph_size] = {}
            tmp_results = {}
            counter = {}
            for i in range(iterations_per_graph_size):
                for ants_number in results[daemon][graph_size][i]:
                    total = 0.0
                    for j in range(iterations_per_test):
                        total += results[daemon][graph_size][i][ants_number][j]
                    results[daemon][graph_size][i][ants_number] = total / len(
                        results[daemon][graph_size][i][ants_number])
                    if tmp_results.get(ants_number, None) is None:
                        tmp_results[ants_number] = results[daemon][graph_size][i][ants_number]
                        counter[ants_number] = 1
                    else:
                        tmp_results[ants_number] += results[daemon][graph_size][i][ants_number]
                        counter[ants_number] += 1
            for k in tmp_results.keys():
                final_results[daemon][graph_size][k] = tmp_results[k] / counter[k]

    x = list(final_results["local_search"].keys())
    y = [[], []]
    for daemon in daemon_actions:
        if daemon == "local_search":
            index = 0
        else:
            index = 1
        for graph_size in final_results[daemon].keys():
            y[index].append((final_results[daemon][graph_size][graph_size // 2] + final_results[daemon][graph_size][
                graph_size] + final_results[daemon][graph_size][graph_size * 2]) / 3)
    plt.plot(x, y[0], "bo:", label="local_search")
    plt.plot(x, y[1], "ro:", label="pheromone_update")
    plt.xlabel("Liczba wierzchołków")
    plt.xticks(x, x)
    plt.ylabel("Czas wykonywania [sekundy]")
    plt.legend(loc='best', shadow=True, fontsize='small')
    plt.title("Średni czas wykonywania w zależności od rozmiaru grafu.")
    plt.savefig("test_local_search_" + time.ctime().replace(" ", "_").replace(":", "_") + ".png")
    plt.show()

    remove_auto_graphs()


def test_compare_bf_aco(iterations_per_test=5, iterations_per_graph_size=5, graph_density=0.2, graph_sizes=(15, 23, 1)):
    results_aco = {}
    results_bf = {}

    for graph_size in range(graph_sizes[0], graph_sizes[1], graph_sizes[2]):
        results_aco[graph_size] = {}
        results_bf[graph_size] = {}
        for i in range(iterations_per_graph_size):
            name = generate_input(graph_size, graph_density)
            graph = read_graph(name)
            results_aco[graph_size][i] = {}
            results_bf[graph_size][i] = {}
            for ants_number in [graph_size // 2, graph_size, graph_size * 2]:
                results_aco[graph_size][i][ants_number] = {}
                results_bf[graph_size][i][ants_number] = {}
                for j in range(iterations_per_test):
                    aco = AntColonyOptimization(graph=graph, ants_num=ants_number, ls_flag=True)
                    start_time = time.time()
                    aco.run(1000)
                    end_time = time.time() - start_time
                    results_aco[graph_size][i][ants_number][j] = end_time
                    start_time = time.time()
                    brute_force(graph)
                    end_time = time.time() - start_time
                    results_bf[graph_size][i][ants_number][j] = end_time

    final_results_aco = {}
    final_results_bf = {}
    for graph_size in range(graph_sizes[0], graph_sizes[1], graph_sizes[2]):
        final_results_aco[graph_size] = {}
        final_results_bf[graph_size] = {}
        tmp_results_aco = {}
        tmp_results_bf = {}
        counter_aco = {}
        counter_bf = {}
        for i in range(iterations_per_graph_size):
            for ants_number in results_aco[graph_size][i]:
                total_aco = 0.0
                for j in range(iterations_per_test):
                    total_aco += results_aco[graph_size][i][ants_number][j]
                results_aco[graph_size][i][ants_number] = total_aco / len(results_aco[graph_size][i][ants_number])
                total_bf = 0.0
                for j in range(iterations_per_test):
                    total_bf += results_bf[graph_size][i][ants_number][j]
                results_bf[graph_size][i][ants_number] = total_bf / len(results_bf[graph_size][i][ants_number])
                if tmp_results_aco.get(ants_number, None) is None:
                    tmp_results_aco[ants_number] = results_aco[graph_size][i][ants_number]
                    counter_aco[ants_number] = 1
                else:
                    tmp_results_aco[ants_number] += results_aco[graph_size][i][ants_number]
                    counter_aco[ants_number] += 1
                if tmp_results_bf.get(ants_number, None) is None:
                    tmp_results_bf[ants_number] = results_bf[graph_size][i][ants_number]
                    counter_bf[ants_number] = 1
                else:
                    tmp_results_bf[ants_number] += results_bf[graph_size][i][ants_number]
                    counter_bf[ants_number] += 1
        for k in tmp_results_aco.keys():
            final_results_aco[graph_size][k] = tmp_results_aco[k] / counter_aco[k]
            final_results_bf[graph_size][k] = tmp_results_bf[k] / counter_aco[k]

    x = list(final_results_aco.keys())
    y = [[], []]
    for graph_size in final_results_aco.keys():
        y[0].append((final_results_aco[graph_size][graph_size // 2] + final_results_aco[graph_size][graph_size] +
                     final_results_aco[graph_size][graph_size * 2]) / 3)
        y[1].append((final_results_bf[graph_size][graph_size // 2] + final_results_bf[graph_size][graph_size] +
                     final_results_bf[graph_size][graph_size * 2]) / 3)
    plt.plot(x, y[0], "bo:", label="ACO")
    plt.plot(x, y[1], "ro:", label="Brute force")
    plt.xlabel("Liczba wierzchołków")
    plt.xticks(x, x)
    plt.ylabel("Czas wykonywania [sekundy]")
    plt.legend(loc='best', shadow=True, fontsize='small')
    plt.title("Średni czas wykonywania w zależności od rozmiaru grafu.")
    plt.savefig("test_compare_bf_aco_" + time.ctime().replace(" ", "_").replace(":", "_") + ".png")
    plt.show()

    remove_auto_graphs()

