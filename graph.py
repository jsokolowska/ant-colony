from vertex import Vertex


class Graph:
    def __init__(self):
        self.vertices = []

    def add_edge(self, start_vertex, end_vertex, weight):
        if (start_vertex or end_vertex) >= len(self.vertices):
            raise IndexError
        if weight < 0:
            raise ValueError
        neighbour = {end_vertex: weight}
        self.vertices[start_vertex].add_neighbours(neighbour)
        neighbour = {start_vertex: weight}
        self.vertices[end_vertex].add_neighbours(neighbour)

    def add_vertex(self, count=1):
        for i in range(count):
            self.vertices.append(Vertex())
