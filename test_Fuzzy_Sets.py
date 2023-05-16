import unittest
import Fuzzy_Sets as FS
import numpy as np


class Test_Fuzzy_Sets(unittest.TestCase):

    @unittest.skip("demonstrating skipping")
    def test_nothing(self):
        self.fail("shouldn't happen")

    def test_FS_create(self):
        M_1 = np.array([0, 1, 2, 3, 7, 10, 6, 4, 3, 1])

        self.assertEqual(FS.FS_create(M_1, None),
                         {1: 0.0, 2: 0.1, 3: 0.2, 4: 0.3, 5: 0.7, 6: 1.0, 7: 0.6, 8: 0.4, 9: 0.3, 10: 0.1})
        self.assertEqual(FS.FS_create(np.array([1, 1, 1, 1, 1]), None),
                         {1: 1, 2: 1, 3: 1, 4: 1, 5: 1})
        self.assertEqual(FS.FS_create(M_1,
                                      np.array(["Mark", "Peter", "Robert", "John"])),
                         {'Mark': 0.0,
                          'Peter': 0.3333333333333333,
                          'Robert': 0.6666666666666666,
                          'John': 1.0})

        self.assertAlmostEqual(FS.FS_create(M_1,
                                            np.array(["Mark", "Peter", "Robert", "John"]))['Peter'],
                               0.3333333)

        with self.assertRaises(Exception):
            FS.FS_create(np.array([0.3, 1, 1, 3, 7]),
                         np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))

    @unittest.expectedFailure
    def test_fail_FS_create(self):
        self.assertEqual(FS.FS_create([0, 1, 2, 3, 7, 10, 6, 4, 3, 1], None),
                         {1: 0.0, 2: 0.1, 3: 0.2, 4: 0.3, 5: 0.7, 6: 1.0, 7: 0.6, 8: 0.4, 9: 0.3, 10: 0.1})

        self.assertEqual(FS.FS_create(np.array([0, 0, 0, 0, 0])),
                         {1: 0, 2: 0, 3: 0, 4: 0, 5: 0})

    def test_MS_trapezoid(self):
        self.assertCountEqual(FS.MS_trapezoid(np.array([1, 2, 3, 4, 5, 6]), 2, 4, 4, 6),
                              ([0.,  0.,  0.5, 1.,  0.5, 0.]))

    def test_FS_union(self):
        M_1 = np.array([0, 1, 2, 3, 7, 10, 6, 4, 3, 1])
        M_2 = np.array([0, 4, 6, 10, 4, 1, 0, 0, 0, 0])
        F_1 = FS.FS_create(M_1, None)
        F_2 = FS.FS_create(M_2, None)

        self.assertEqual(FS.FS_union(F_1, F_2),
                         {1: 0.0, 2: 0.4, 3: 0.6, 4: 1.0, 5: 0.7,
                          6: 1.0, 7: 0.6, 8: 0.4, 9: 0.3, 10: 0.1})

        with self.assertRaises(Exception):
            FS.FS_union(F_1, FS.FS_create(np.array([0, 0, 0]), None, False))


if __name__ == '__main__':
    unittest.main()
