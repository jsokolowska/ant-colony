import unittest
from vertex import Vertex


class MyTestCase(unittest.TestCase):
    # this test is currently not working - im figuring that out
    def test_id_uniqueness(self):
        temp1 = Vertex()
        temp1.add_neighbours({0: 10})
        self.assertEqual(Vertex.instances_created, 1)
        self.assertEqual(temp1.id, 0)
        temp2 = Vertex()
        temp2.add_neighbours({0: 20})
        self.assertEqual(temp2.id, 1)
        self.assertEqual(Vertex.instances_created, 2)

    def test_add_neighbours(self):
        temp = Vertex()
        new_neighbour = {1: 10}
        temp.add_neighbours(new_neighbour)
        self.assertDictEqual(temp.neighbours, new_neighbour)


if __name__ == '__main__':
    unittest.main()
