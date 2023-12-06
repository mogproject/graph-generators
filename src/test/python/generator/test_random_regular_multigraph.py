import unittest
from random import Random

from generator.random_regular_multigraph import random_regular_multigraph


class TestRandomRegularMultigraph(unittest.TestCase):
    """Tests random_regular_multigraph module."""

    def test_random_regular_multigraph(self):
        rand = Random(12345)

        for _ in range(5):
            for d in [0, 1, 2, 3, 5, 99, 100]:
                for n in [0, 1, 2, 3, 5, 10, 99, 100]:
                    G = random_regular_multigraph(n, d, rand)
                    assert len(G) == n
                    if n <= 1:
                        for i in range(n):
                            self.assertEqual(G.degree(i), 0)
                    else:
                        if d * n % 2 == 0:
                            for i in range(n):
                                self.assertEqual(G.degree(i), d)
                        else:
                            cnt = 0
                            for i in range(n):
                                self.assertLessEqual(d - 1, G.degree(i))
                                self.assertLessEqual(G.degree(i), d)
                                if G.degree(i) != d:
                                    cnt += 1
                            self.assertEqual(cnt, 1)
