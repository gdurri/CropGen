import pandas as pd
import random

class JobsServerClientMock:
  WATER_USE = 'WaterUse'
  YIELD = 'Yield'

  def __init__(self, logger, config):
    self.logger = logger
    self.config = config

  def _run(self, job_id, params, outputNames, table):
    results = {
      self.WATER_USE: [random.randint(0, 1000)], 
      self.YIELD: [random.randint(0, 1000)]
    }
    return results