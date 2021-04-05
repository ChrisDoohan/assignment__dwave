import unittest
from ising import AdjacencyMatrix

class TestAdjacencyMatrix(unittest.TestCase):
    def test_that_data_can_be_stored_and_retrieved(self):
        j = AdjacencyMatrix()
        j.put_weight(0, 1, 1)
        j.put_weight(0, 2, 2)
        j.put_weight(2, 3, 3)
        j.put_weight(2, 4, 4)

        # Check basic retention
        self.assertEqual(j.get_weight(0, 1), 1)

        # Check transverse
        self.assertEqual(j.get_weight(1, 0), 1)

        # Check neighbor lookup is reasonable
        self.assertEqual(set(j.neighbors(2)), set([0, 3, 4]))

        self.assertEqual(set(j.nodes()), set([0, 1, 2, 3, 4]))

    def test_that_depth_map_and_parents_are_properly_built(self):
        j = AdjacencyMatrix()
        j.put_weight(0, 1, 0)
        j.put_weight(1, 2, 0)
        j.put_weight(2, 3, 0)
        j.put_weight(2, 4, 0)

        depth_map, parent_map = j.get_meta_maps_from_a_given_root(0)
        self.assertEqual(depth_map[0], {0})
        self.assertEqual(depth_map[1], {1})
        self.assertEqual(depth_map[2], {2})
        self.assertEqual(depth_map[3], {3, 4})

        self.assertEqual(parent_map[4], 2)
        self.assertEqual(parent_map[3], 2)
        self.assertEqual(parent_map[2], 1)
        self.assertEqual(parent_map[1], 0)

        # We should now be able to specify a different root and get different depth labels
        # Take 4 as the new root.
        depth_map, parent_map = j.get_meta_maps_from_a_given_root(4)
        self.assertEqual(depth_map[0], {4})
        self.assertEqual(depth_map[1], {2})
        self.assertEqual(depth_map[2], {1, 3})
        self.assertEqual(depth_map[3], {0})

        self.assertEqual(parent_map[0], 1)
        self.assertEqual(parent_map[1], 2)
        self.assertEqual(parent_map[2], 4)
        self.assertEqual(parent_map[3], 2)

if __name__ == '__main__':
    unittest.main()
