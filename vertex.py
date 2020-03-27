class Vertex:
    instances_created = 0

    def __init__(self):
        self.id = Vertex.instances_created
        Vertex.instances_created = Vertex.instances_created + 1
        print("Updated vertex count: " + str(Vertex.instances_created))
        self.neighbours = {}

    def add_neighbours(self, neighbours):
        self.neighbours.update(neighbours)
