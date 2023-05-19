import unittest

from parameterized import parameterized
from test.test_base import TestBase
from lib.aggregate_functions.failure_risk_function import FailureRiskFunction
from lib.models.cgm.apsim_result import ApsimResult

class TestAggregateFunction():
    def __init__(self, values):
        self.values = values
    
    def get_param_by_index(self, index):
        return self.values[index]


class FailureRiskFunctionTests(TestBase):

    @parameterized.expand([
        ("<",  "10",    0, 0.75),
        ("<",  "1",     0, 0),
        ("<",  "8",     0, 0.5),
        ("<=", "10",    0, 1),
        ("<=", "8",     0, 0.75),
        (">",  "5",     0, 0.5),
        (">",  "1",     0, 0.75),
        (">=", "8",     0, 0.5),
        (">=", "3",     0, 0.5),
        ("==", "2",     0, 0.25),
        ("==", "100",   0, 0),
        ("==", "-90",   0, 0),
        ("!=", "8",     0, 0.75),
        ("!=", "100",   0, 1)
    ])
    def test_calculate(self, operator, param, apsim_output_index, expected):
        # Arrange
        aggregate_function = TestAggregateFunction([operator, param])
        results_for_individual = [
            self.create_apsim_result([1, 0, 0, 0, 0]),
            self.create_apsim_result([2, 0, 0, 0, 0]),
            self.create_apsim_result([8, 0, 0, 0, 0]),
            self.create_apsim_result([10, 0, 0, 0, 0])
        ]

        # Act
        actual = FailureRiskFunction.calculate(aggregate_function, results_for_individual, apsim_output_index)

        # Assert
        self.assertEqual(actual, expected, f"operator: {operator} param: {param} expected: {expected} actual: {actual}")


    def create_apsim_result(self, values):
        apsim_result = ApsimResult()
        apsim_result.Values = values
        return apsim_result

if __name__ == "__main__":
    unittest.main()
