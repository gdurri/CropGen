#
# This represents an output from APSIM, after the multiplier has
# been applied and it contains only the information needed to send
# a ResultsMessage
#
class ApsimOutput():
    #
    # Constructor
    #
    def __init__(self, simulation_id, simulation_name):
        self.simulation_id = simulation_id
        self.simulation_name = simulation_name
        self.outputs = []