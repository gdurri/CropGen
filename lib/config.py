import json
import os

class Config:
  def __init__(self):

    relative_path = '../config/config.json'
    current_script_dir = os.path.dirname(os.path.realpath(__file__))
    config_file_full_path = os.path.join(current_script_dir, relative_path)

    with open(config_file_full_path) as json_config_file:
        data = json.load(json_config_file)    
    
    self.jobs_base_url = data['jobsBaseUrl']
    self.sim_gen_url = data['simGenUrl']
    self.use_mock_job_server_client = data['useMockJobServerClient']
    self.show_graphs_when_generated = data['showGraphsWhenGenerated']
    # Override this config setting if we are running inside of a docker 
    # container.
    if os.environ.get('RUNNING_IN_DOCKER', False):
      self.show_graphs_when_generated = False


  def _get_sim_gen_url(self):
    return os.path.join(self.jobs_base_url, self.sim_gen_url)