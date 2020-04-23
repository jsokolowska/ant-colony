# Ant Colony
Finding shortest path between two vertices in weighted graphs using ACO - Ant Colony Optimization algorithm.

## Installation and usage
Download the project files and open linux terminal in the main project folder. Execute the following command:
```bash
python -m src.main [filepath]
```
Supply path to .txt file with the graph in place of [filepath]. Input file must contain a list of graph edges in following format:
```textmate
vertex vertex edge_weight
...
vertex vertex edge_weight
start end
```
Where vertex is vertex label and star and end are labels of the vertices that constitute both ends of the path. 

For a list of all options please read the information displayed by following commands
```bash
python -m src.main --help
```
or 
```bash
python -m src.main -h
```
