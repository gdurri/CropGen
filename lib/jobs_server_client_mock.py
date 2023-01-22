import random

class JobsServerClientMock:
  WATER_USE = 'WaterUse'
  YIELD = 'Yield'
  RANDOM_INT_MIN = 0
  RANDOM_INT_MAX = 1000

  def __init__(self, logger, config):
    self.logger = logger
    self.config = config

  def _run(self, job_id, params, outputNames, table):
    results = {
      self.WATER_USE: [random.randint(self.RANDOM_INT_MIN, self.RANDOM_INT_MAX)], 
      self.YIELD: [random.randint(self.RANDOM_INT_MIN, self.RANDOM_INT_MAX)]
    }

    self.logger._log_debug(
      "{} run called with job_id: {}. Returning mock result: {}".format(
        self.__class__.__name__,
        job_id,
        results
        )
      )

    return results