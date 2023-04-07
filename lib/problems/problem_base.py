from pymoo.core.problem import Problem
import logging
import numpy as NumPy

from lib.cgm_server.cgm_client_factory import CGMClientFactory
from lib.utils.results_publisher import ResultsPublisher

#
# The base class for Problems, provides some useful problem specific functionality.
#
class ProblemBase(Problem):
    #
    # Constructor
    #
    def __init__(self, config, run_job_request):
        # Member variables
        self.config = config
        self.run_job_request = run_job_request
        self.run_errors = []
        self.current_iteration_id = 1
        self.is_multi_year = False

        self.results_publisher = ResultsPublisher(
            run_job_request.IterationResultsUrl,
            run_job_request.FinalResultsUrl,
            config.results_publisher_timeout_seconds
        )

        self.cgm_server_client = CGMClientFactory.create(run_job_request.CGMServerHost, run_job_request.CGMServerPort, config)
        
        total_inputs = run_job_request.get_total_inputs()
        total_outputs = run_job_request.get_total_outputs()
        lower_bounds = self._construct_input_lower_bounds()
        upper_bounds = self._construct_input_upper_bounds()

        logging.info(
            "Constructing Problem with %d inputs and %d outputs. Setting the lowerbounds to: %s and the upperbounds to: %s",
            total_inputs,
            total_outputs,
            lower_bounds,
            upper_bounds
        )

        super().__init__(
            n_var = total_inputs,
            n_obj = total_outputs,
            xl = NumPy.array(lower_bounds),
            xu = NumPy.array(upper_bounds)
        )

    #
    # Create the input lower bounds by using the values from the run job request
    # input min values.
    #
    def _construct_input_lower_bounds(self):
        input_lower_bounds = []
        for input in self.run_job_request.Inputs:
            input_lower_bounds.append(input.Min)
        return input_lower_bounds
    
    #
    # Create the input lower bounds by using the values from the run job request
    # input min values.
    #
    def _construct_input_upper_bounds(self):
        input_upper_bounds = []
        for input in self.run_job_request.Inputs:
            input_upper_bounds.append(input.Max)
        return input_upper_bounds

    #
    # Constructs a data frame containing the input and output data
    # using the input and output columns.
    #
    def get_combined_inputs_outputs(self):
        columns = []
        for input in self.run_job_request.get_input_names():
            columns.append(input)
        for output in self.run_job_request.get_apsim_output_names():
            columns.append(output)
        return columns
    