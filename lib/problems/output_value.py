class OutputValue():
    #
    # Constructor
    #
    def __init__(self, raw_apsim_output, output):
        self.raw_apsim_output = raw_apsim_output
        self.output = output

    #
    # Gets the name of the output.
    #
    def get_output_name(self):
        return self.output.ApsimOutputName

    #
    # Gets the output value for use in the minimise algorithm.
    #
    def get_output_value_for_algorithm(self):
        if self.output.Maximise:
            return -abs(self.raw_apsim_output)
        return self.raw_apsim_output
    
    #
    # Gets the output value for use in results.
    #
    def get_output_value_for_results(self):
        return self.raw_apsim_output * self.output.Multiplier