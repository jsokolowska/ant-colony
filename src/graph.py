from src.vertex import Vertex


class Graph:
    def __init__(self):
        self.vertices = {}
        self.start = None
        self.end = None

    def add_edge(self, start_vertex: str, end_vertex: str, weight: int, pheromone=0.0):
        if weight <= 0:
            raise ValueError("Edge's weight must be greater than 0")
        if start_vertex not in self.vertices:
            self.add_vertex(start_vertex)
        if end_vertex not in self.vertices:
            self.add_vertex(end_vertex)

        neighbour = {end_vertex: {"weight": weight, "pheromone": pheromone}}
        self.vertices[start_vertex].add_neighbours(neighbour)

        neighbour = {start_vertex: {"weight": weight, "pheromone": pheromone}}
        self.vertices[end_vertex].add_neighbours(neighbour)

    def add_vertex(self, name: str):
        self.vertices[name] = Vertex(name)

    def __str__(self):
        string = ""
        if self.start is not None:
            string += "Start vertex: " + str(self.start) + "\n"
        if self.end is not None:
            string += "End vertex: " + str(self.end) + "\n"
        for name, vertex in self.vertices.items():
            string = string + name + " : "
            for neigh, weight in vertex.neighbours.items():
                string = string + neigh + "-" + str(weight) + ", "
            string += "\n"
        return string

    def set_start_vertex(self, start_id):
        if self.is_vertex(start_id):
            self.start = self.vertices[start_id]

    def set_end_vertex(self, end_id):
        if self.is_vertex(end_id):
            self.end = self.vertices[end_id]

    def is_vertex(self, name: str):
        return name in self.vertices
