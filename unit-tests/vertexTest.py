import unittest
from vertex import Vertex


class MyTestCase(unittest.TestCase):
    def test_id_uniqueness(self):
        temp = Vertex()
        self.assertEqual(Vertex.instances_created, 1)
        temp2 = Vertex()
        self.assertEqual(Vertex.instances_created, 2)

    def test_add_neighbours(self):
        temp = Vertex()
        new_neighbour = {1: 10}
        temp.add_neighbours(new_neighbour)
        self.assertDictEqual(temp.neighbours, new_neighbour)


if __name__ == '__main__':
    unittest.main()
