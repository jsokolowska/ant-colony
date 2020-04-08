class Vertex:

    def __init__(self, name: str):
        self.id = name
        self.neighbours = {}

    def add_neighbours(self, neighbours: {str: {str: object}}):
        if self.id not in neighbours:
            self.neighbours.update(neighbours)
