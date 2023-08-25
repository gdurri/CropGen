import os
import sys
import psutil
import logging

#
# A helper class for restarting this application.
#
class Restart():
    
    #
    # Restarts this program.
    #
    @staticmethod
    def perform_restart():
        try:
            python = sys.executable
            # Use sys.argv to pass the original command-line arguments
            os.execv(python, [python] + sys.argv)
        except Exception:
            logging.exception("Failed to restart program")