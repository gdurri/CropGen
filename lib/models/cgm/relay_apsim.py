from lib.models.common.model import Model

#
# An input ID wrapper. Python doesn't let you pass an int by reference. This acts a simple
# wrapper for this as objects are passed by reference.
#
class InputIdWrapper():
    #
    # Constructor
    #
    def __init__(self, id):
        self.id = id

    #
    # Getter
    #
    def get_id(self): return self.id

    #
    # Setter
    #
    def set_id(self, id): self.id = id

    #
    # Increments the id by 1
    #
    def increment_id(self): self.id += 1

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
        input_id = InputIdWrapper(RelayApsim.INPUT_START_INDEX)

        # Iterate over each environment type that was supplied.
        for environment_type in environment_types:
            self.add_inputs_for_env_type(environment_type, season_date_generator, generated_input_values, input_id)

    #
    # Adds all of the input values, simulation names and system property values, for a specific env type.
    #
    def add_inputs_for_env_type(self, environment_type, season_date_generator, generated_input_values, input_id):
        for environment in environment_type.Environments:
            for season in environment.Seasons:
                start_date = season_date_generator.generate_start_date_from_season(season)
                end_date = season_date_generator.generate_end_date_from_season(season)

                for individual in range(0, len(generated_input_values)):
                    self.SystemPropertyValues.append([str(input_id.get_id()), start_date, end_date])
                    self.SimulationNames.append([str(input_id.get_id()), environment_type.Name])

                    self.add_inputs_for_individual(input_id.get_id(), generated_input_values[individual])
                    input_id.increment_id()

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
