import logging
import os
import random

class Jobs:
  def __init__(self, config):
    self.config = config

  def _run(self):
    simGenUrl = os.path.join(self.config.jobsBaseUrl, self.config.simGenUrl)
    logging.info(simGenUrl)
    return random.randint(0, 10000)