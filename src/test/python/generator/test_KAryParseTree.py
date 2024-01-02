import unittest

from generator.KAryParseTree import KAryParseTree


class TestKAryParseTree(unittest.TestCase):
    """Tests KAryParseTree class."""

    def test_constructor(self):
        t = KAryParseTree(2, 6)

        self.assertEqual(len(t), 11)
        self.assertListEqual(t.bounds, [
            (0, 6),
            (0, 4), (4, 6),
            (0, 2), (2, 4), (4, 5), (5, 6),
            (0, 1), (1, 2), (2, 3), (3, 4)
        ])
        self.assertEqual(t.nodes_by_level(0), range(0, 1))
        self.assertEqual(t.nodes_by_level(1), range(1, 3))
        self.assertEqual(t.nodes_by_level(2), range(3, 7))
        self.assertEqual(t.nodes_by_level(3), range(7, 11))
        self.assertEqual(t.nodes_by_level(4), range(0, 0))

        t = KAryParseTree(2, 1)

        self.assertEqual(len(t), 1)
        self.assertListEqual(t.bounds, [
            (0, 1)
        ])

        t = KAryParseTree(2, 4)

        self.assertEqual(len(t), 7)
        self.assertListEqual(t.bounds, [
            (0, 4),
            (0, 2), (2, 4),
            (0, 1), (1, 2), (2, 3), (3, 4)
        ])

        t = KAryParseTree(4, 17)

        self.assertEqual(len(t), 23)
        self.assertListEqual(t.bounds, [
            (0, 17),
            (0, 5), (5, 9), (9, 13), (13, 17),
            (0, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 16), (16, 17),
            (0, 1), (1, 2)
        ])

        t = KAryParseTree(4, 15)

        self.assertEqual(len(t), 20)
        self.assertListEqual(t.bounds, [
            (0, 15),
            (0, 4), (4, 8), (8, 12), (12, 15),
            (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15),
        ])
