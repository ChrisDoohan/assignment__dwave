import math
import os
import unittest
from ising import AdjacencyMatrix, GraphParser, IsingTreeSolver

class TestIsingTreeSolver(unittest.TestCase):
    def test_case_of_two_spins_in_constant_b_field(self):
        # Both spins are expected to align down
        h = {0: 1, 1: 1}
        coupling = AdjacencyMatrix()
        coupling.put_weight(0, 1, 0)
        solver = IsingTreeSolver(coupling, h)
        energy, spins = solver.run()

        self.assertEqual(energy, -2)
        self.assertEqual(spins, {0: -1, 1: -1})

    def test_case_of_two_coupled_spins(self):
        # With no external field, spins should anti-align if the coupling constant is positive
        coupling = AdjacencyMatrix()
        coupling.put_weight(0, 1, 1)
        solver = IsingTreeSolver(coupling, {})
        energy, spins = solver.run()

        self.assertEqual(energy, -1)
        self.assertTrue(spins[0] == -spins[1])

    def test_case_provided_in_pdf(self):
        file_name = os.path.join('test', 'files', 'given_example.txt')
        parser = GraphParser(file_name)
        h = parser.external_field_vector()
        j = parser.coupling_matrix()

        solver = IsingTreeSolver(j, h)
        energy, spins = solver.run()
        self.assertEqual(energy, -4.0)
        self.assertEqual(spins, {0: 1, 1: -1, 2: 1, 3: 1})

    def test_that_chosing_any_root_node_produces_same_result(self):
        # This is just a sanity check on the procedure itself
        file_name = os.path.join('test', 'files', 'given_example.txt')
        parser = GraphParser(file_name)
        h = parser.external_field_vector()
        j = parser.coupling_matrix()

        solver = IsingTreeSolver(j, h)
        energy0, _ = solver.run(0)
        energy1, _ = solver.run(1)
        energy2, _ = solver.run(2)
        energy3, _ = solver.run(3)

        # All energies should be identical
        self.assertEqual(len(set([energy0, energy1, energy2, energy3])), 1)

    def test_four_spins_with_mixed_coupling_and_field(self):
        # The expected values in this test case came from brute forcing all spin configs.
        # The edge configuration has depth 2 instead of 1 as provided in the pdf
        h = {0: -2.2,
            1: 5.1,
            2: 3.3,
            3: 1}
        coupling = AdjacencyMatrix()

        coupling.put_weight(0, 1, 2.1)
        coupling.put_weight(1, 2, 1)
        coupling.put_weight(1, 3, 5.5)

        solver = IsingTreeSolver(coupling, h)
        energy, spins = solver.run()

        self.assertAlmostEqual(energy, -16.2)
        self.assertEqual(spins, {0: 1, 1: -1, 2: -1, 3: 1})

if __name__ == '__main__':
    unittest.main()
