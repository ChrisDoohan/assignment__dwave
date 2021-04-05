import os
import sys

from ising import GraphParser, IsingTreeSolver

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please pass file path as first parameter')
        sys.exit()

    file_name = sys.argv[1]
    if not os.path.isfile(file_name):
        print('Could not find file named "{}"'.format(file_name))
        sys.exit()

    parser = GraphParser(file_name)
    h = parser.external_field_vector()
    j = parser.coupling_matrix()

    solver = IsingTreeSolver(j, h)
    min_energy, spin_config = solver.run()
    spin_string = ''.join(['+' if spin_config[k] == 1 else '-' for k in sorted(spin_config.keys())])
    print(min_energy)
    print(spin_string)
