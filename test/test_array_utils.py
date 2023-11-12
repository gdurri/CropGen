import unittest

from parameterized import parameterized
from test.test_base import TestBase
from test.helpers.apsim_result_helper import ApsimResultHelper
from lib.utils.array_utils import ArrayUtils

class ArrayUtilsTests(TestBase):
    def test_split_arr_with_valid_max(self):
        # Arrange
        arr = [20, 23, 55, 77, 86, 99, 106]
        max_val = 5
        expected_result = [[20, 23, 55, 77, 86], [99, 106]]
 
        # Act
        result = ArrayUtils._split_arr(arr, max_val)
 
        # Assert
        self.assertEqual(result, expected_result)
 
    def test_split_arr_with_max_greater_than_array_length(self):
        # Arrange
        arr = [20, 23, 55, 77, 86, 99, 106]
        max_val = 10
        expected_result = [arr]  # The whole array should be in a single sub-array
 
        # Act
        result = ArrayUtils._split_arr(arr, max_val)
 
        # Assert
        self.assertEqual(result, expected_result)
 
if __name__ == '__main__':
    unittest.main()