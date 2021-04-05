import os
import unittest
from ising import GraphParser

class TestGraphParser(unittest.TestCase):
    def test_import_of_example_file(self):
        file_name = os.path.join('test', 'files', 'given_example.txt')
        gp = GraphParser(file_name)

        h = gp.external_field_vector()
        j = gp.coupling_matrix()

        # All expected values defined by given_example.txt
        self.assertEqual(len(h), 3.0)
        self.assertEqual(h[0], -1.0)
        self.assertEqual(h[1], -1.0)
        self.assertEqual(h[2], -1.0)

        self.assertEqual(len(j), 4)
        self.assertEqual(j.get_weight(0, 1), 1.0)
        self.assertEqual(j.get_weight(1, 0), 1.0)
        self.assertEqual(j.get_weight(3, 1), 1.0)


if __name__ == '__main__':
    unittest.main()
