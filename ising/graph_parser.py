from .adjacency_matrix import AdjacencyMatrix

class GraphParser:
    def __init__(self, file_name):
        self.j = AdjacencyMatrix()
        self.h = {}

        f = open(file_name, 'r')

        while line := f.readline():
            line_identifier = line[0]
            if line_identifier in ('c', 'p', '\n'):
                continue

            self._ingest_line(line)

        f.close()

    def _ingest_line(self, line):
        vals = line.split()
        row, col, weight = int(vals[0]), int(vals[1]), float(vals[2])

        if row == col:
            self.h[row] = weight
        else:
            self.j.put_weight(row, col, weight)

    def coupling_matrix(self):
        return self.j

    def external_field_vector(self):
        return self.h
