"""
    Created by: Joanna Sokołowska
    Date of creation: 22.04.2020
    Github: https://github.com/jsokolowska
"""
import argparse
from pathlib import Path
from src.ant_colony_optimization import AntColonyOptimization
from src.graph_input import read_graph_from_file

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description='''\
Ant Colony Optimization - finding shortest path in weighted graph
------------------------------------------------------------------''')
parser.add_argument('filepath', help="path to file with input graph")
parser.add_argument('-ls', '--local_search', action='store_true', default=False,
                    help="enables local_search algorithm that will increase exploitation of local minima")
parser.add_argument('-diff', action='store', type=float, default=0.5,
                    help="works only if local search is enabled, only the solutions worse than "
                         "the best solution by no more than given percent will be used for pheromone update, "
                         "must be between 0 and 1.")
parser.add_argument('-q', action='store', type=float, default=1,
                    help="single ant pheromone multiplier.")
parser.add_argument('-ro', action='store', type=float, default=0.1,
                    help="decides how quickly pheromones on the graph edges fade, "
                         " must be between 0 and 1,"
                         " smaller value means slower fading, bigger means quicker fading")
parser.add_argument('-a', '--ants_num', action='store', type=int, default=50,
                    help="number of ants used to generate solutions")
parser.add_argument('-i', '--iterations', action='store', type=int, default=1000,
                    help='max number of algorithm iterations.')
parser.add_argument('-p', '--persistence', action='store', type=int, default=5,
                    help='after how many iterations with no improvement to the best found path will calculations stop.')
args = parser.parse_args()

if not Path(args.filepath).is_file():
    print("Input file not found\n")
else:
    graph = read_graph_from_file(args.filepath)
    aco = AntColonyOptimization(graph=graph, ants_num=args.ants_num, q_param=args.q, ro_param=args.ro, ls_flag=args.local_search,
                                diff_percentage=args.diff, persistence_param=args.persistence)
    path = aco.run(args.iterations)
    print("Ścieżka:" + str(path[0]) + "\nKoszt: " + str(path[1]))

