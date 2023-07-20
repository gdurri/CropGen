import json
import os

from lib.models.common.model import Model
from lib.models.cgm.relay_apsim import RelayApsim
from lib.utils.json_helper import JsonHelper

class RelayApsimFromFile(Model):

    #
    # Constructor.
    #
    def __init__(self):
        self.relay_apsim = self._create_relay_apsim(self._parse())

    #
    # Parses the config JSON file and stores it in memory.
    #
    def _parse(self):
        config_file_full_path = os.path.join(os.path.dirname(__file__), 'relay_apsim.json')
        
        with open(config_file_full_path) as json_config_file:
            json_object = json.load(json_config_file)

        return json_object

    #
    # Creates the request
    #
    def _create_relay_apsim(self, json_object):
        errors = []
        job_id = JsonHelper.get_attribute(json_object, 'JobID', errors)
        individuals = JsonHelper.get_attribute(json_object, 'Individuals', errors)
        inputs = JsonHelper.get_attribute(json_object, 'Inputs', errors)

        relay_apsim = RelayApsim(job_id, individuals)
        relay_apsim.Inputs = inputs

        return relay_apsim
