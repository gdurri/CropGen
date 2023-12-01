import unittest

from parameterized import parameterized
from test.test_base import TestBase
from lib.utils.array_utils import ArrayUtils

class ArrayUtilsTests(TestBase):
    @parameterized.expand([
        ([20, 23, 55, 77, 86, 99, 106], 5, [[20, 23, 55, 77, 86], [99, 106]]),
        ([20, 23, 55, 77, 86, 99, 106], 10, [[20, 23, 55, 77, 86, 99, 106]]),
        ([20, 23, 55, 77, 86, 99, 106], 7, [[20, 23, 55, 77, 86, 99, 106]]),
        ([20, 23, 55, 77, 86, 99, 106], 8, [[20, 23, 55, 77, 86, 99, 106]]),
        ([], 5, []),
    ])
    def test_split_arr(self, arr, max_val, expected_result):
        # Act
        result = ArrayUtils._split_arr(arr, max_val)
        # Assert
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()