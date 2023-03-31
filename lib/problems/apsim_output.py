class OutputValue():
    #
    # Constructor
    #
    def __init__(self, raw_apsim_output, maximise, multiplier):
        self.raw_apsim_output = raw_apsim_output
        self.maximise = maximise
        self.multiplier = multiplier

    #
    # Gets the output value for use in the minimise algorithm.
    #
    def get_output_value_for_algorithm(self):
        if self.maximise:
            return -abs(self.raw_apsim_output)
        return self.raw_apsim_output
    
    #
    # Gets the output value for use in results.
    #
    def get_output_value_for_results(self):
        return self.raw_apsim_output * self.multiplier

#
# This represents an output from APSIM, after the multiplier has
# been applied and it contains only the information needed to send
# a ResultsMessage
#
class ApsimOutput():
    #
    # Constructor
    #
    def __init__(self):
        self.simulation_id = ''
        self.simulation_name = ''
        self.outputs = []