import logging
import os
import random

from config import Config

class Jobs:
  def __init__(self):
    self.config = Config()

  def _run(self):
    simGenUrl = os.path.join(self.config.jobsBaseUrl, self.config.simGenUrl)
    logging.info(simGenUrl)
    return random.randint(0, 10000)