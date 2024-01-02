__all__ = 'KAryParseTree'


class KAryParseTree:
    """
    Example:
      k=2, num_leaves=6:
                  0
               /     `
             1         2
          /    `      / `
         3      4    5   6
        / `    / `  [4] [5]
       7   8  9  10
      [0] [1][2] [3]

      i: node id
      [j]: corresponds to vertex j
    """

    def __init__(self, k: int, num_leaves: int) -> None:
        assert k >= 2
        assert num_leaves >= 1

        # find the number of deepest leaves
        num_leaves_full = 1
        num_nodes_full = 1
        while num_leaves_full < num_leaves:
            num_leaves_full *= k
            num_nodes_full += num_leaves_full

        if num_leaves == num_leaves_full:
            # full k-ary tree
            num_bottom_leaves = num_leaves_full
        else:
            y = (num_leaves - num_leaves_full // k - k) // (k - 1) + 1
            num_bottom_leaves = num_leaves - (num_leaves_full // k - y - 1)

        num_nodes = num_nodes_full - (num_leaves_full - num_bottom_leaves)

        # initialize vertex ranges
        bounds = [(0, 0) for _ in range(num_nodes)]  # type: list[tuple[int, int]]

        for j in range(num_leaves):
            if j < num_bottom_leaves:
                i = num_nodes - num_bottom_leaves + j
            else:
                i = num_nodes - num_leaves + (j - num_bottom_leaves)
            bounds[i] = (j, j + 1)

        self.root = 0
        self.k = k
        self.num_leaves = num_leaves
        self.num_nodes = num_nodes

        # compute all vertex ranges
        for i in self.internal_nodes_bottom_up():
            bounds[i] = (bounds[self.left(i)][0], bounds[self.right(i)][1])

        self.bounds = bounds

        # compute node range for each leevel
        j = self.root
        levels = []
        while not self.is_leaf(j):
            nxt = self.left(j)
            levels += [range(j, nxt)]
            j = self.left(j)
        levels += [range(j, num_nodes)]
        self.levels = levels

    def __len__(self) -> int:
        return self.num_nodes

    def is_leaf(self, i: int) -> bool:
        return i >= self.num_nodes - self.num_leaves

    def left(self, i: int) -> int:
        """Returns the node id of the leftmost child."""
        assert 0 <= i < self.num_nodes - self.num_leaves
        return i * self.k + 1

    def right(self, i: int) -> int:
        """Returns the node id of the rightmost child"""
        assert 0 <= i < self.num_nodes - self.num_leaves
        return min(self.num_nodes, self.left(i) + self.k) - 1

    def internal_nodes_bottom_up(self) -> range:
        return range(self.num_nodes - self.num_leaves - 1, -1, -1)

    def nodes_by_level(self, level: int) -> range:
        if level >= len(self.levels):
            return range(0, 0)
        return self.levels[level]

    def leaves(self) -> range:
        return range(self.num_nodes - self.num_leaves, self.num_nodes)

    def vertex_range(self, i: int) -> range:
        assert 0 <= i < self.num_nodes
        return range(self.bounds[i][0], self.bounds[i][1])

    def children(self, i: int) -> range:
        assert 0 <= i < self.num_nodes
        return range(self.left(i), self.right(i) + 1)

    def num_children(self, i: int) -> int:
        assert 0 <= i < self.num_nodes
        return self.right(i) + 1 - self.left(i)
