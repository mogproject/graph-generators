from random import Random
import networkx as nx

from generator.KAryParseTree import KAryParseTree
from generator.random_regular_multigraph import random_regular_multigraph


def random_near_modular_graph(n: int, k: int, d: int, rand: Random) -> nx.Graph:
    t = KAryParseTree(k, n)
    G = nx.empty_graph(n)

    for i in t.internal_nodes_bottom_up():
        # create a metagraph
        meta = random_regular_multigraph(t.num_children(i), d, rand)

        # add an edge between random vertices
        for x, y in meta.edges():
            u = rand.choice(t.vertex_range(t.left(i) + x))
            v = rand.choice(t.vertex_range(t.left(i) + y))
            G.add_edge(u, v)
    return G
