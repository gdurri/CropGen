import pandas as Pandas

class JobsServerClientMock:
  WATER_USE = 'WaterUse'
  YIELD = 'Yield'

  def __init__(self, logger, config):
    self.logger = logger
    self.config = config
    self.sim_gen_url = config._get_sim_gen_url()

  def _run(self, job_id, params, outputNames, table):
    # Create a mock of the results
    lst = [[self.WATER_USE, 25], [self.YIELD, 30]]
    # creating df object with columns specified
    return Pandas.DataFrame(lst, columns =[self.WATER_USE, self.YIELD]) 

