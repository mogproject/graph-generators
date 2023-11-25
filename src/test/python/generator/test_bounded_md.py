import unittest
from random import Random

import networkx as nx
from generator.bounded_md import modular_width_bounded_graph


class TestBoundedMW(unittest.TestCase):
    """Tests bounded_mw module."""

    def test_modular_width_bounded_graph(self):
        rand = Random(12345)
        density = []
        for _ in range(5):
            for n in [10, 100, 1000]:
                G = modular_width_bounded_graph(rand, n, 5, 0.5)
                assert len(G) == n
                density += [nx.density(G)]

        assert 0.4 < sum(density) / len(density) < 0.6
