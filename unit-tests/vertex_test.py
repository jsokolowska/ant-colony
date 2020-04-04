import unittest
from src.vertex import Vertex


class MyTestCase(unittest.TestCase):
    # this test is currently not working - im figuring that out
    def test_id_uniqueness(self):
        temp1 = Vertex("A")
        temp1.add_neighbours({"A": 10})
        self.assertEqual(Vertex.instances_created, 1)
        self.assertEqual(temp1.id, "A")
        temp2 = Vertex("B")
        temp2.add_neighbours({"A": 20})
        self.assertEqual(temp2.id, "B")
        self.assertEqual(Vertex.instances_created, 2)

    def test_add_neighbours(self):
        temp = Vertex("C")
        new_neighbour = {"B": 10}
        temp.add_neighbours(new_neighbour)
        self.assertDictEqual(temp.neighbours, new_neighbour)


if __name__ == '__main__':
    unittest.main()
