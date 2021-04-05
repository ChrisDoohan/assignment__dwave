# D-Wave Take-home Assignment
This repository supplies a solution to the problem supplied in the PDF present in this directory.

# Running the Code
This implementation is vanilla Python3. After pulling the code, `cd` into the repo root and run `python -m unittest` in order to ensure that there is no issue with the environment.

The solver can be invoked as follows
```shell
python ./run_ising.py ./test/files/given_example.txt
```
where the second argument is any file conforming to the spec outlined in the `PDF`.

# Assumptions
- All input lines are either blank, start with "c" or "p", or they specify some weight. No other type of line exists in the input file.
- All vertex labels in the input file are integers.
- All weights are integers or floats, but are real valued.
- The input edges represent a tree. There are no cycles, and there are no unconnected vertices.
- The input graph will require no more than 4GB of RAM to run, using an algorithm with storage proportional to n*log(n) via some constant.

# Discussion of Design Decisions
## Data Representation
A few convenience classes have been included in order to make the main routine easy to read. Edges are represented in a class called `AdjacencyMatrix`, which is actually just a couple of hash maps underneath and a custom interface on top. This means that the sparse nature of the coupling matrix is taken advantage of to diminish storage. Because it is stored in a hash map rather than in a two dimensional array, the storage required for the J matrix scales linearly with the number of edges rather than quadratically with the number of vertices. This also allows constant time to look up a vertex's neighbors.

## Algorithm Notes
I am aware that this can be done using recursion, but I chose an (also n*log(n)) iterative approach that starts at the deepest part of the tree and works its way layer by layer back toward the tree root. I made this decision, not only because it's easier to reason about, but because it prevents stack overflow on the main path and saves memory on stack frame instantiation.

Memoization is done on the output of the `IsingTreeSolver.subtree_optimum` method, which returns both the minimum subtree energy and the spin state of the subtree root in a convenience struct. Memoization is done using the `@lru_cache` decorator, which is provided in Python's standard `functools` module. I've set the max size of this cache at 40,000 outputs, as I've calculated that this is a cache size of about 4GB and should be a reasonable upper bound under normal circumstances, but this can be increased if traversing larger trees is desired.
