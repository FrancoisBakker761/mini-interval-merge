import unittest

from mini_interval_merge import Interval, intersect, merge, subtract


class TestMerge(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(merge([]), ())

    def test_single(self):
        self.assertEqual(merge([(0, 1)]), (Interval(0, 1),))

    def test_disjoint(self):
        self.assertEqual(
            merge([(0, 1), (3, 4)]),
            (Interval(0, 1), Interval(3, 4)),
        )

    def test_touching_merge(self):
        # Half-open intervals that touch are merged.
        self.assertEqual(merge([(0, 1), (1, 2)]), (Interval(0, 2),))

    def test_overlapping_merge(self):
        self.assertEqual(merge([(0, 3), (1, 4)]), (Interval(0, 4),))

    def test_contained(self):
        self.assertEqual(merge([(0, 10), (2, 3)]), (Interval(0, 10),))

    def test_unsorted_input(self):
        self.assertEqual(
            merge([(5, 6), (0, 2), (1, 3)]),
            (Interval(0, 3), Interval(5, 6)),
        )

    def test_duplicates(self):
        self.assertEqual(merge([(0, 1), (0, 1)]), (Interval(0, 1),))

    def test_empty_intervals_dropped(self):
        self.assertEqual(merge([(2, 2), (0, 1)]), (Interval(0, 1),))

    def test_accepts_interval_objects(self):
        self.assertEqual(
            merge([Interval(0, 1), Interval(1, 2)]),
            (Interval(0, 2),),
        )


class TestIntersect(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(intersect([], [(0, 1)]), ())
        self.assertEqual(intersect([(0, 1)], []), ())

    def test_disjoint(self):
        self.assertEqual(intersect([(0, 1)], [(2, 3)]), ())

    def test_touching_yields_nothing(self):
        # [0, 1) and [1, 2) meet at a point, which is not an interval.
        self.assertEqual(intersect([(0, 1)], [(1, 2)]), ())

    def test_overlap(self):
        self.assertEqual(
            intersect([(0, 3)], [(1, 4)]),
            (Interval(1, 3),),
        )

    def test_multiple(self):
        self.assertEqual(
            intersect([(0, 10)], [(1, 2), (4, 6)]),
            (Interval(1, 2), Interval(4, 6)),
        )

    def test_normalizes_inputs(self):
        self.assertEqual(
            intersect([(0, 2), (1, 4)], [(3, 5)]),
            (Interval(3, 4),),
        )


class TestSubtract(unittest.TestCase):
    def test_empty_b(self):
        self.assertEqual(subtract([(0, 1)], []), (Interval(0, 1),))

    def test_empty_a(self):
        self.assertEqual(subtract([], [(0, 1)]), ())

    def test_no_overlap(self):
        self.assertEqual(
            subtract([(0, 1)], [(2, 3)]),
            (Interval(0, 1),),
        )

    def test_touching_does_not_remove(self):
        # b ends exactly where a starts; nothing is removed.
        self.assertEqual(
            subtract([(1, 2)], [(0, 1)]),
            (Interval(1, 2),),
        )

    def test_cut_middle(self):
        self.assertEqual(
            subtract([(0, 10)], [(3, 5)]),
            (Interval(0, 3), Interval(5, 10)),
        )

    def test_cut_start(self):
        self.assertEqual(
            subtract([(0, 10)], [(0, 4)]),
            (Interval(4, 10),),
        )

    def test_cut_end(self):
        self.assertEqual(
            subtract([(0, 10)], [(6, 10)]),
            (Interval(0, 6),),
        )

    def test_remove_all(self):
        self.assertEqual(subtract([(0, 10)], [(0, 10)]), ())

    def test_multiple_cuts(self):
        self.assertEqual(
            subtract([(0, 10)], [(2, 3), (5, 6)]),
            (Interval(0, 2), Interval(3, 5), Interval(6, 10)),
        )

    def test_normalizes_inputs(self):
        self.assertEqual(
            subtract([(0, 5), (3, 8)], [(4, 6)]),
            (Interval(0, 4), Interval(6, 8)),
        )


if __name__ == "__main__":
    unittest.main()
