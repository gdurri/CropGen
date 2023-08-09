from lib.models.common.model import Model

#
# A CGM Server request object that invokes APSIM runs, calling update parameters and passing in 
# the input values that will override the input traits that were sent in the InitWorkers request.
#
class RelayApsim(Model):
    INPUT_START_INDEX = 0

    #
    # Constructor
    #
    def __init__(
        self, 
        job_id,
        individuals
    ):
        self.JobID = job_id
        self.Individuals = individuals
        self.Inputs = []
        self.SimulationNames = []
        self.SystemPropertyValues = []

    #
    # Adds all of the input values, simulation names and system property values, for all of the env types.
    #
    def add_inputs_for_env_typing(self, environment_types, season_date_generator, generated_input_values):
        for input_id in range(0, len(generated_input_values)):

            input_values = generated_input_values[input_id]

            # Iterate over each environment type that was supplied.
            for environment_type in environment_types:
                self.add_inputs_for_env_type(environment_type, season_date_generator, input_id, input_values)

    #
    # Adds all of the input values, simulation names and system property values, for a specific env type.
    #
    def add_inputs_for_env_type(self, environment_type, season_date_generator, input_id, input_values):
        for environment in environment_type.Environments:
            for season in environment.Seasons:
                start_date = season_date_generator.generate_start_date_from_season(season)
                end_date = season_date_generator.generate_end_date_from_season(season)

                self.SystemPropertyValues.append([str(input_id), start_date, end_date])
                self.SimulationNames.append([str(input_id), environment_type.Name])

                self.add_inputs_for_individual(input_id, input_values)
    
    #
    # Adds all of the inputs.
    #
    def add_inputs(self, generated_input_values):
        for individual in range(RelayApsim.INPUT_START_INDEX, len(generated_input_values)):
            self.add_inputs_for_individual(individual, generated_input_values[individual])


    #
    # Adds all of the inputs.
    #
    def add_inputs_for_individual(self, individual, inputs):

        # Add the iteration id to the beginning of the array. 
        # We use the individual index for a convenient auto incrementing id.
        values = [individual]

        # Iterate over all of the input values that were passed in,
        # adding each one to the values array
        for input_value in inputs:
            values.append(input_value)

        # Now add the complete list of values which will contain the iteration
        # id, followed by all of the input values.
        self.Inputs.append(values)
    
    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__
