import logging

from lib.models.cgm.relay_apsim import RelayApsim
from lib.problems.problem_base import ProblemBase
from lib.utils.date_time_helper import DateTimeHelper

#
# Represents a Problem
#
class Problem(ProblemBase):

    #
    # Construct problem with the given dimensions and variable ranges
    #
    def __init__(self, config, run_job_request, cgm_server_client):
        super().__init__(config, run_job_request, cgm_server_client)

    #
    # Iterate over each population and perform calculations.
    #
    def _evaluate(self, variable_values_for_population, out_objective_values, *args, **kwargs):
        if self.run_errors:
            super()._initialize_algorithm_array(out_objective_values)
            return

        logging.info("Processing APSIM iteration (%d of %d) with %d individuals", 
            self.current_iteration_id, 
            self.run_job_request.Iterations,
            len(variable_values_for_population)
        )

        start_time = DateTimeHelper.get_date_time()

        response = self._perform_relay_apsim_request(variable_values_for_population)

        if not super()._handle_evaluate_value_for_population(response, out_objective_values, variable_values_for_population):
            super()._initialize_algorithm_array(out_objective_values)
            return

        seconds_taken_one_iteration = DateTimeHelper.get_elapsed_seconds_since(start_time)
        estimated_seconds_remaining = (self.run_job_request.Iterations - self.current_iteration_id) * seconds_taken_one_iteration

        logging.info("Finished processing APSIM iteration: %d. Time taken: %s. Estimated finish date time: %s (%s)",  
            self.current_iteration_id, 
            DateTimeHelper.seconds_to_hhmmss_ms(seconds_taken_one_iteration),
            DateTimeHelper.add_seconds_to_datetime_now(estimated_seconds_remaining),
            DateTimeHelper.seconds_to_hhmmss_ms(estimated_seconds_remaining)
        )

        # Increment our iteration ID.
        self.current_iteration_id += 1

    #
    # Creates the relay apsim request.
    #
    def _perform_relay_apsim_request(self, variable_values_for_population):

        if (self.config.max_individuals_in_one_relay_apsim_request > 0 and 
            self.config.max_individuals_in_one_relay_apsim_request < len(variable_values_for_population)
        ):
            return self._perform_relay_apsim_staggered_requests(variable_values_for_population)
        else:
            return self._perform_relay_apsim_one_request(variable_values_for_population)
    
    #
    # Creates the relay apsim request.
    #
    def _perform_relay_apsim_staggered_requests(self, variable_values_for_population):
        
        max_individuals = self.config.max_individuals_in_one_relay_apsim_request

        # Calculate the number of chunks based on the max_individuals value
        num_chunks = (len(variable_values_for_population) + max_individuals - 1) // max_individuals

        if (self.config.max_individuals_in_one_relay_apsim_request > 0):
            logging.info("Splitting individuals into %d separate RelayApsim requests", num_chunks)

        # Initialize an empty list to store the responses
        responses = []
        individual = RelayApsim.INPUT_START_INDEX

        # Split the variable_values_for_population into chunks and process each chunk
        for chunk_index in range(num_chunks):
            # Calculate the start and end index for each chunk
            start_index = chunk_index * max_individuals
            end_index = (chunk_index + 1) * max_individuals
            inputs_to_process = variable_values_for_population[start_index:end_index]

            # Create a new RelayApsim object for each chunk
            relay_apsim_request = RelayApsim(self.run_job_request.JobID, len(inputs_to_process))

            for input_index in range(len(inputs_to_process)):
                relay_apsim_request.add_inputs_for_individual(individual, inputs_to_process[input_index])
                individual += 1

            # Call _call_relay_apsim for the current chunk and store the response
            response = self._call_relay_apsim(relay_apsim_request)
            responses.append(response)

        response = super()._stitch_responses_into_response(responses)
        return response
    
    #
    # Creates the relay apsim request.
    #
    def _perform_relay_apsim_one_request(self, variable_values_for_population):
        
        relay_apsim_request = RelayApsim(self.run_job_request.JobID, len(variable_values_for_population))
        relay_apsim_request.add_inputs(variable_values_for_population)
        response = self._call_relay_apsim(relay_apsim_request)
        return response
