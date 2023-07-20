from lib.problems.output_value import OutputValue
from lib.problems.apsim_output import ApsimOutput

from lib.aggregate_functions.aggregate_function_calculator import AggregateFunctionCalculator

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
        config, 
        apsim_simulation_id_str, 
        apsim_simulation_name_str,
        results_for_individual,
        all_algorithm_outputs,
        all_results_outputs
    ):
        total_outputs = run_job_request.get_total_outputs()
        algorithm_outputs = []
        
        apsim_output = ApsimOutput(apsim_simulation_id_str, apsim_simulation_name_str)

        for output_index in range(0, total_outputs):
            request_output = run_job_request.get_output_by_index(output_index)

            # If there is no output or we're not optimising this output, then just skip and move onto the next one.
            if not request_output or not request_output.Optimise: continue

            for aggregate_function in request_output.AggregateFunctions:
                aggregate_function_calculator = AggregateFunctionCalculator(config, apsim_simulation_name_str, aggregate_function)
                raw_output_value = aggregate_function_calculator.calculate_output_value(results_for_individual, output_index)
                output_value = OutputValue(
                    raw_output_value, 
                    aggregate_function.DisplayName, 
                    aggregate_function.Maximise, 
                    aggregate_function.Multiplier
                )

                algorithm_outputs.append(output_value.get_output_value_for_algorithm())
                apsim_output.outputs.append(output_value)

        all_algorithm_outputs.append(algorithm_outputs)
        all_results_outputs.append(apsim_output)
