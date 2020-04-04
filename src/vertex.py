class Vertex:
    # instances_created = 0

    def __init__(self, name: str):
        self.id = name
        # Vertex.instances_created = Vertex.instances_created + 1
        # print("Vertex: ", name, " added. Updated vertex count: " + str(Vertex.instances_created))
        self.neighbours = {}

    def add_neighbours(self, neighbours: {str: {str: object}}):
        if self.id not in neighbours:
            self.neighbours.update(neighbours)
