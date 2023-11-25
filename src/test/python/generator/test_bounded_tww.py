import unittest
from random import Random

import networkx as nx
from generator.bounded_tww import twin_width_bounded_graph


class TestBoundedTWW(unittest.TestCase):
    """Tests bounded_mw module."""

    def test_modular_width_bounded_graph(self):
        rand = Random(12345)

        for _ in range(5):
            for n in [10, 100, 1000]:
                G = twin_width_bounded_graph(rand, n, 5, 2)
                assert len(G) == n
                assert G.number_of_edges() > n // 2
