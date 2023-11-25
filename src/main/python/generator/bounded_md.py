from random import Random
from itertools import combinations, product

import networkx as nx
from generator.KAryParseTree import KAryParseTree

def modular_width_bounded_graph(rand: Random, n: int, mw: int, p: float) -> nx.Graph:
    t = KAryParseTree(mw, n)
    G = nx.empty_graph(n)

    for i in t.internal_nodes_bottom_up():
        for j, k in combinations(t.children(i), 2):
            if rand.random() < p:
                # create a biclique
                for x, y in product(t.vertex_range(j), t.vertex_range(k)):
                    G.add_edge(x, y)
    return G
