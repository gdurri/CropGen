import numpy as NumPy

from lib.problems.output_value import OutputValue
from lib.utils.constants import Constants

#
# Helper for processing the single year results.
#
class MultiYearResultsProcessor():
    
    #
    # Handles the results for a single year sim.
    #
    @staticmethod
    def process_results(
        run_job_request, 
        out_objective_values, 
        iteration_results_message,
        results_for_individual
    ):
        assert(out_objective_values)
        assert(len(results_for_individual) > 1)
        assert(iteration_results_message)

        apsim_result = results_for_individual[0]

        simulation_id = apsim_result.SimulationID
        simulation_name = apsim_result.SimulationName
        total_outputs = len(apsim_result.Values)

        algorithm_outputs = []
        result_outputs = []

        for output_index in range(0, total_outputs):
            raw_apsim_output = apsim_result.Values[output_index]
            request_output = run_job_request.get_output_by_index(output_index)

            assert(request_output)

            output_value = OutputValue(raw_apsim_output, request_output)
            algorithm_outputs.append(output_value.get_output_value_for_algorithm())
            result_outputs.append((output_value.get_output_name(), output_value.get_output_value_for_results()))

        # Feed the results back into the algorithm so that it can continue advancing...
        out_objective_values[Constants.OBJECTIVE_VALUES_ARRAY_INDEX] = NumPy.array(algorithm_outputs)   