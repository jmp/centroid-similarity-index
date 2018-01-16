from unittest import TestCase

from csi import csi, find_nearest, calculate_mapping


class FindNearestTest(TestCase):
    def test_find_nearest(self):
        self.assertEqual((1, 1), find_nearest((0, 0), [(1, 1), (1, 2), (1, 3)]))
        self.assertEqual((1, 1), find_nearest((0, 0), [(1, 2), (1, 1), (1, 3)]))


class CalculateMappingTest(TestCase):
    def test_calculate_mapping_trivial(self):
        mapping = calculate_mapping([(0, 0)], [(1, 1)])
        self.assertDictEqual(mapping, {
            (0, 0): (1, 1),
        })

    def test_calculate_mapping_symmetric(self):
        cluster1 = [(0, 0), (0, 1)]
        cluster2 = [(-1, 0), (0, 2)]
        mapping1 = calculate_mapping(cluster1, cluster2)
        mapping2 = calculate_mapping(cluster2, cluster1)
        self.assertDictEqual(mapping1, {
            (0, 0): (-1, 0),
            (0, 1): (0, 2),
        })
        self.assertDictEqual(mapping2, {
            (-1, 0): (0, 0),
            (0, 2): (0, 1),
        })

    def test_calculate_mapping_asymmetric(self):
        cluster1 = [(0, 0), (0, 1)]
        cluster2 = [(-1, 0), (0, 2), (0, 3)]
        mapping1 = calculate_mapping(cluster1, cluster2)
        mapping2 = calculate_mapping(cluster2, cluster1)
        self.assertDictEqual(mapping1, {
            (0, 0): (-1, 0),
            (0, 1): (0, 2),
        })
        self.assertDictEqual(mapping2, {
            (-1, 0): (0, 0),
            (0, 2): (0, 1),
            (0, 3): (0, 1),
        })


class CsiTest(TestCase):
    def test_csi_same(self):
        cluster1 = [(5, 0), (0, 5)]
        cluster2 = [(6, 0), (0, 6)]
        solution1 = {
            (2, 2): cluster1,
            (3, 3): cluster2,
        }
        solution2 = {
            (2, 2): cluster1,
            (3, 3): cluster2,
        }
        self.assertEqual(1, csi(solution1, solution2))

    def test_csi_some_different(self):
        cluster1 = [(5, 0), (4, 1), (3, 2), (2, 2), (5, 1), (5, 3)]
        cluster2 = [(15, 0), (14, 1), (13, 2), (12, 2), (15, 1), (15, 3)]
        solution1 = {
            (2, 2): cluster1,
            (13, 1): cluster2,
        }
        solution2 = {
            (2, 2): cluster1,
            (3, 1): cluster2,
        }
        self.assertEqual(0.75, csi(solution1, solution2))

    def test_csi_all_different(self):
        cluster1 = [(5, 0), (4, 1), (3, 2), (2, 2), (5, 1), (5, 3)]
        cluster2 = [(15, 0), (14, 1), (13, 2), (12, 2), (15, 1), (15, 3)]
        solution1 = {
            (2, 2): cluster1,
            (13, 1): cluster2,
        }
        solution2 = {
            (13, 1): cluster1,
            (2, 2): cluster2,
        }
        self.assertEqual(0, csi(solution1, solution2))
