from collections import defaultdict, namedtuple
from functools import lru_cache

# Convenience struct
MinimumNodeConfig = namedtuple('MinimumNodeConfig', ['energy', 'spin'])

class IsingTreeSolver:
    def __init__(self, coupling_matrix, external_field_vector):
        self.j = coupling_matrix
        self.h = external_field_vector

    def run(self, root=None):
        if len(self.h) == 0 and len(self.j) == 0:
            self.print_trivial_solution()
            return

        if not root:
            # If not specified, tree root is arbitrarily chosen as the lowest numbered node
            self.root = sorted(list(self.h.keys()) + list(self.j.nodes()))[0]
        self.nodes_at_depth, self.parents = self.j.get_meta_maps_from_a_given_root(self.root)

        minimum_energy = self.compute_optimum_for_all_subtrees().energy
        minimum_spin_state = self.compile_final_state()

        return minimum_energy, minimum_spin_state

    def compute_optimum_for_all_subtrees(self):
        # Start with leaves (largest depth)
        depth = sorted(self.nodes_at_depth.keys())[-1]

        while depth > 0:
            outermost_unoptimized_nodes = self.nodes_at_depth[depth]
            for node in outermost_unoptimized_nodes:
                self.subtree_optimum(node, 1)
                self.subtree_optimum(node, -1)
            depth -= 1

        # In the case of depth=0, there is only the root node, and this has no parent, so
        # both "parent" up and "parent" down give the minimum state.
        return self.subtree_optimum(self.root, 1)

    # Returns lowest energy and the spin of this node that leads to it
    # Assumes optima of all children have already been determined
    @lru_cache(maxsize=40000)
    def subtree_optimum(self, node, parent_spin):
        # get the energy of the self against the external field. sign tbd
        external_field_energy = self.h.get(node, 0)

        # get the coupling energy of the self against the parent
        parent = self.parents.get(node)
        parent_coupling_energy = parent_spin * self.j.get_weight(node, parent)

        parent_and_external_energy = external_field_energy + parent_coupling_energy

        self_upspin_child_coupling_energy = 0
        self_downspin_child_coupling_energy = 0
        for child in [x for x in self.j.neighbors(node) if x != parent]:
            self_upspin_child_coupling_energy += self.subtree_optimum(child, 1).energy
            self_downspin_child_coupling_energy += self.subtree_optimum(child, -1).energy

        self_upspin_total_energy = parent_and_external_energy + self_upspin_child_coupling_energy
        self_downspin_total_energy = -parent_and_external_energy + self_downspin_child_coupling_energy

        # Determine minimum and return it, which logs it in this function's cache
        if self_upspin_total_energy < self_downspin_total_energy:
            return MinimumNodeConfig(self_upspin_total_energy, 1)
        else:
            return MinimumNodeConfig(self_downspin_total_energy, -1)

    def compile_final_state(self):
        # Start at stored root state and walk the best path to the leaves
        state = self.subtree_optimum(self.root, 1)
        all_spins = {self.root: state.spin}

        def store_subtree_spins(parent, node):
            all_spins[node] = self.subtree_optimum(node, all_spins[parent]).spin

            for child in [c for c in self.j.neighbors(node) if c != parent]:
                store_subtree_spins(node, child)

        # Kick off the traversal
        for child in self.j.neighbors(self.root):
            store_subtree_spins(self.root, child)

        return all_spins

    def print_trivial_solution(self):
        print(0)
        print()
