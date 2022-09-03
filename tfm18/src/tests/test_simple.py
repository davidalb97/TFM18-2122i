# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
import math
import unittest
from typing import Tuple

from tfm18.src.main.algorithm.BaseAlgorithm import BaseAlgorithm
from tfm18.src.main.algorithm.BasicApproach import BasicApproach
from tfm18.src.main.algorithm.HistoryBasedApproach import HistoryBasedApproach


def doStuff():
    pass


class TestSimple(unittest.TestCase):

    def test_add_one(self):
        self.assertEqual(3 + 3, 6)

    def test1(self):
        a: BaseAlgorithm = HistoryBasedApproach(
            N=1,
            delta=1.0,
            min_timestamp_step_ms=8,
            min_instance_energy=3000,
            basic_approach=BasicApproach()
        )
        b: HistoryBasedApproach = a
        print("test %s" % b.min_instance_energy)

    def get_mosaic(self, key_count: int) -> Tuple[list[list[str]], list[str]]:
        func_index = 0
        grapth_slots = math.floor(math.pow(func_index + 1, 2)/4)
        while key_count > grapth_slots:
            func_index += 1
            grapth_slots = math.floor(math.pow(func_index + 1, 2)/4)

        L = int(func_index - ((func_index / 2) - ((math.pow(-1, func_index) - 1) / - 4)))
        if L * L < key_count:
            C = L + 1
        else:
            C = L

        mosaic: list[list[str]] = []
        mosaic_unique_keys: list[str] = []
        empty_sentinel_key = '.'
        curr_index = 0
        for _ in range(L):
            line: list[str] = []
            for _ in range(C):
                key: str
                if curr_index >= key_count:
                    key = empty_sentinel_key
                else:
                    key = "%d" % curr_index
                    mosaic_unique_keys.append(key)
                line.append(key)
                line.append(key)
                curr_index += 1
            mosaic.append(line)

        return mosaic, mosaic_unique_keys

    def test3(self):
        mosaic_setup, unique_mosaic_keys = self.get_mosaic(9)
        print()
        # self.assertEqual(len(mosaic), 4)

    def test2(self):
        # https://oeis.org/A002620
        my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        len_my_list = len(my_list)
        result: list[list[int]]
        index = 0
        _index = math.floor(math.pow(index, 2)/4)

        # L = index ç
        # C =
        # 0x0, sqrt(0) = oo, index = 0, L = index - 0 = 0, C = index - 0 = 0
        # [  ]
        if len_my_list <= 1:
            doStuff()
        # 1x1, sqrt(1) = 1, index = 1, L = index - 0 = 1, C = index - 0 = 1
        # [ 0 ]
        if len_my_list <= 1:
            doStuff()
        # 2x1, sqrt(2) = 1.41, index = 2, L = index - 1 = 1, C = index - 0 = 2
        # [ 0 1 ]
        if len_my_list <= 2:
            doStuff()
        # 2x2, sqrt(4) = 2, index = 3, L = index - 1 = 2, C = index - 1 = 2
        # [ 0 1 ]
        # [ 2 3 ]
        elif len_my_list <= 4:
            doStuff()
        # 2x3, sqrt(6) = 2.44, index = 4, L = index - 2 = 2, C = index - 1 = 3
        # [ 0 1 2 ]
        # [ 3 4 5 ]
        elif len_my_list <= 6:
            doStuff()
        # 3x3, sqrt(9) = 3, index = 5, L = index - 2 = 3, C = index - 2 = 3
        # [ 0 1 2 ]
        # [ 3 4 5 ]
        # [ 6 7 8 ]
        elif len_my_list <= 9:
            doStuff()
        # 3x4, sqrt(12) = 3.46, index = 6, L = index - 3 = 3, C = index - 2 = 4
        # [ 0  1  2  3 ]
        # [ 4  5  6  7 ]
        # [ 8  9  10 11 ]
        elif len_my_list <= 12:
            doStuff()
        # 4x4, sqrt(16) = 4, index = 7, L = index - 3 = 4, C = index - 3 = 4
        # [ 0  1  2  3  ]
        # [ 4  5  6  7  ]
        # [ 8  9  10 11 ]
        # [ 12 13 14 15 ]
        elif len_my_list <= 16:
            doStuff()
        # 4x5, sqrt(20) = 4.47, index = 8, L = index - 4 = 4, C = index - 3 = 5
        # [ 0  1  2  3  4  ]
        # [ 5  6  7  8  9  ]
        # [ 10 11 12 13 14 ]
        # [ 15 16 17 18 19 ]
        elif len_my_list <= 20:
            doStuff()
        # 5x5, sqrt(25) = 5, index = 9, L = index - 4 = 5, C = index - 4 = 5
        # [ 0  1  2  3  4  ]
        # [ 5  6  7  8  9  ]
        # [ 10 11 12 13 14 ]
        # [ 15 16 17 18 19 ]
        # [ 20 21 22 23 24 ]
        elif len_my_list <= 25: # 5x6:
            doStuff()

if __name__ == '__main__':
    unittest.main()
