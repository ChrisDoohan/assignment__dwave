from collections import defaultdict

class AdjacencyMatrix:
    def __init__(self):
        self.dict = defaultdict(dict)

    def put_weight(self, row, col, weight):
        self.dict[row][col] = self.dict[col][row] = weight

    def get_weight(self, row, col):
        if row not in self.dict or col not in self.dict[row]:
            return 0
        else:
            return self.dict[row][col]

    def neighbors(self, node):
        return self.dict[node].keys()

    def nodes(self):
        return self.dict.keys()

    # Given a specific root, this function walks the tree in order to return a map of all
    # nodes at a given depth, as well as a map of each node to its parent
    def get_meta_maps_from_a_given_root(self, root):
        depth_to_nodes = defaultdict(set)
        depth_to_nodes[0] = set([root])
        node_to_parent = {}
        
        def record_neighbor_of(parent, node, node_depth):
            node_to_parent[node] = parent
            depth_to_nodes[node_depth].add(node)

            for neighbor in self.neighbors(node):
                if neighbor != parent:
                    record_neighbor_of(node, neighbor, node_depth + 1)

        # Kick off traversal at the root
        for neighbor in self.neighbors(root):
            record_neighbor_of(root, neighbor, 1)

        return depth_to_nodes, node_to_parent


    def __repr__(self):
        return str(self.dict)

    def __len__(self):
        return len(self.dict)
