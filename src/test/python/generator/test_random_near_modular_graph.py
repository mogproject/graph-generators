import unittest
from random import Random

import networkx as nx
from generator.random_near_modular_graph import random_near_modular_graph


class TestRandomNearModularGraph(unittest.TestCase):
    """Tests random_near_modular_graph module."""

    def test_random_near_modular_graph(self):
        rand = Random(12345)

        for _ in range(5):
            for n in [10, 100, 1000]:
                G = random_near_modular_graph(n, 5, 2, rand)
                self.assertEqual(len(G), n)
                self.assertGreater(G.number_of_edges(), n // 2)

        G = random_near_modular_graph(9, 3, 2, rand)
        self.assertEqual(len(G), 9)
        self.assertEqual(G.number_of_edges(), 12)

        G = random_near_modular_graph(27, 3, 2, rand)
        self.assertEqual(len(G), 27)
        self.assertEqual(G.number_of_edges(), 39)

        for _ in range(5):
            G = random_near_modular_graph(27, 3, 4, rand)
            self.assertEqual(len(G), 27)
            self.assertGreaterEqual(G.number_of_edges(), 48)
            self.assertLessEqual(G.number_of_edges(), 54)
