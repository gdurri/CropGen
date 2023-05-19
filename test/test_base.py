import unittest
import logging

class TestBase(unittest.TestCase):
    def setUp(self):
        # Configure logging to print to console
        logging.basicConfig(level=logging.ERROR, format="%(message)s")

    def tearDown(self):
        # Reset logging configuration after each test
        logging.basicConfig(level=logging.WARNING)

    def log_to_console(self, message):
        # Log the message to the console during the test
        logging.info(message)