from random import Random
from collections import defaultdict

import networkx as nx
from generator.KAryParseTree import KAryParseTree


def twin_width_bounded_graph(rand: Random, n: int, k: int, d: int) -> nx.Graph:
    t = KAryParseTree(k, n)
    G = nx.empty_graph(n)
    ext_deg: dict[int, int] = defaultdict(int)  # external degrees

    for i in t.internal_nodes_bottom_up():
        children = t.children(i)
        available = set(children)
        safety_count = 0

        while len(available) >= 2 and safety_count < 10:
            # pick random distinct children
            x, y = rand.sample(list(available), 2)

            # add an edge between random vertices
            u = rand.choice(t.vertex_range(x))
            v = rand.choice(t.vertex_range(y))

            if not G.has_edge(u, v):
                G.add_edge(u, v)
                for z in [x, y]:
                    ext_deg[z] += 1
                    if ext_deg[z] >= d:
                        available.remove(z)
                safety_count = 0
            else:
                safety_count += 1  # prevent infinite loops
    return G
