from random import Random
import networkx as nx


def random_regular_multigraph(n: int, d: int, rand: Random) -> nx.MultiGraph:
    """
    Creates a random $d$-regular multigraph on $n$ nodes when $dn$ is even.
    If $dn$ is odd, then outputs a multigraph such that
    one vertex has degree $d-1$, and other $n-1$ vertices have degree $d$.

    A regular multigraph is a multigraph where each node has
    the same number of incident (possibly parallel) edges.
    The resulting graph has no self-loops.

    Time complexity: $O(dn)$.

    @param n: number of vertices
    @param d: maximum degree
    @param rand: Random instance
    """
    assert 0 <= n and 0 <= d

    vertices = list(range(n))  # list of vertices sorted by degree
    deg = [0 for _ in range(n)]  # stores the current degree of each vertex
    deg_idx = [0 if i == 0 else n for i in range(d + 1)]  # index of the first degree-i vertex
    min_deg = 0  # minimum degree
    edges = []

    while deg_idx[d] >= 2:
        # pick two vertices, one of which should have the minimum degree
        u_idx = rand.randint(0, deg_idx[min_deg + 1] - deg_idx[min_deg] - 1)
        v_idx = rand.randint(0, deg_idx[d] - 2)
        if v_idx >= u_idx:
            v_idx += 1
        u_idx, v_idx = min(u_idx, v_idx), max(u_idx, v_idx)
        u, v = vertices[u_idx], vertices[v_idx]

        # add edge uv
        edges += [(u, v)]

        # update degrees
        for k_idx in [v_idx, u_idx]:
            k = vertices[k_idx]
            deg_idx[deg[k] + 1] -= 1
            if deg_idx[deg[k] + 1] == 0:
                min_deg = deg[k] + 1
            swap_with = deg_idx[deg[k] + 1]
            vertices[k_idx], vertices[swap_with] = vertices[swap_with], vertices[k_idx]
            deg[k] += 1

    G = nx.empty_graph(n, create_using=nx.MultiGraph)
    G.add_edges_from(edges)
    return G
