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
        results_for_individual,
        all_algorithm_outputs,
        all_results_outputs
    ):
        assert(len(results_for_individual) > 1)
        
        total_outputs = run_job_request.get_total_outputs()
        algorithm_outputs = []

        for output_index in range(0, total_outputs):
            request_output = run_job_request.get_output_by_index(output_index)

            if not request_output: continue

            for aggregate_function in request_output.AggregateFunctions:
                aggregate_function_calculator = AggregateFunctionCalculator(aggregate_function)
                output_value = aggregate_function_calculator.calculate_output_value(results_for_individual)


        #     output_value = OutputValue(raw_apsim_output, request_output)
        #     algorithm_outputs.append(output_value.get_output_value_for_algorithm())
        #     apsim_output.outputs.append(output_value)

        # all_algorithm_outputs.append(algorithm_outputs)
        # all_results_outputs.append(apsim_output)