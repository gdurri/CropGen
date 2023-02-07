from lib.models.model import Model

#
# Model that represents a run job request sent from the jobs server
#
class RunJobRequest(Model):
    #
    # Constructor. Simply pass the request data for parsing.
    #
    def __init__(self, request_data):
        self.errors = []
        self._parse(request_data)

    #
    # Returns true if there are no errors.
    #
    def is_valid(self):
        return not self.errors

    #
    # Parses the JSON data into this class.
    #
    def _parse(self, body):
        self.errors.clear()
        self.job_id = self._get_attribute(body, 'jobId')
        self.individuals = self._get_attribute(body, 'individuals')
        self.inputs = self._get_attribute(body, 'inputs')
        self.outputs = self._get_attribute(body, 'outputs')

    #
    # Safely extracts the attribute, or appends an error if it isn't present
    # and sets the value to the value_if_not_present (defaulted)
    #
    def _get_attribute(self, body, attribute_name, value_if_not_present=None):
        value = value_if_not_present
        if attribute_name in body:
            value = body[attribute_name]
        else:
            self.errors.append(f"No {attribute_name} specified")
        return value
