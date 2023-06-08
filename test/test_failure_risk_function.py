import unittest

from parameterized import parameterized
from test.test_base import TestBase
from test.apsim_result_helper import ApsimResultHelper
from lib.aggregate_functions.failure_risk_function import FailureRiskFunction

class TestAggregateFunction(TestBase):
    def __init__(self, values):
        self.values = values
    
    def get_param_by_index(self, index):
        param = None
        if len(self.values) > index:
            return self.values[index]
        else:
            super().log_to_console(f"TestAggregateFunction: No value at index: {index}")
        return param


class FailureRiskFunctionTests(TestBase):

    @parameterized.expand([
        ("<",  "10",    0, 0.75),
        ("<",  "1",     0, 0),
        ("<",  "8",     0, 0.5),
        ("<",  "0",     1, 0),

        ("<=", "10",    0, 1),
        ("<=", "8",     0, 0.75),
        ("<=", "8",     2, 1),

        (">",  "5",     0, 0.5),
        (">",  "1",     0, 0.75),
        (">",  "1",     3, 0),

        (">=", "8",     0, 0.5),
        (">=", "3",     0, 0.5),
        (">=", "3",     3, 0),

        ("==", "2",     0, 0.25),
        ("==", "100",   0, 0),
        ("==", "-90",   0, 0),
        ("==", "2",     2, 0),

        ("!=", "8",     0, 0.75),
        ("!=", "100",   0, 1),
        ("!=", "0",     1, 0)
    ])
    def test_calculate(self, operator, param, apsim_output_index, expected):
        # Arrange
        aggregate_function = TestAggregateFunction([operator, param])
        results_for_individual = ApsimResultHelper.create_results_for_individual(
            [1, 2, 8, 10], 0
        )

        # Act
        actual = FailureRiskFunction.calculate(aggregate_function, results_for_individual, apsim_output_index)

        # Assert
        self.assertEqual(actual, expected, f"operator: {operator} param: {param} apsim_output_index: {apsim_output_index} expected: {expected} actual: {actual}")

if __name__ == "__main__":
    unittest.main()
