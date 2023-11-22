import unittest

from parameterized import parameterized
from test.test_base import TestBase
from unittest.mock import Mock
from lib.utils.run_message_validator import RunMessageValidator

class RunMessageValidatorTest(TestBase):
  def setUp(self):
        # Create a mock configuration and server state for testing
        self.config = Mock()
        self.server_state = Mock()
        self.cgm_client_factory = Mock()
 
@parameterized.expand([
        ("123", True),  # Test case with a running job
        ("", False),    # Test case with no running job
    ])
def test_validate_no_jobs_are_currently_running(self, running_job_id, expected_result):
        # Arrange
        validator = RunMessageValidator(self.config, self.server_state)
        self.server_state.get_running_job_id.return_value = running_job_id
 
        # Act
        result = validator._validate_no_jobs_are_currently_running()
 
        # Assert
        self.assertEqual(result, expected_result)
        if not expected_result:
            self.assertEqual(len(validator.get_errors()), 1)
        else:
            self.assertEqual(len(validator.get_errors()), 0)
 
if __name__ == "__main__":
    unittest.main()