from lib.models.model import Model

class RunJobRequest(Model):
    # Constants
    JOB_ID_JSON_ATTRIBUTE = 'jobId'
    INDIVIDUALS_JSON_ATTRIBUTE = 'individuals'
    INPUTS_JSON_ATTRIBUTE = 'inputs'
    OUTPUTS_JSON_ATTRIBUTE = 'outputs'

    def __init__(self, request_data):
        self.errors = []
        self._parse(request_data)

    def _is_valid(self):
        return not self.errors

    def _parse(self, body):
        self.errors.clear()
        self.job_id = self._get_attribute(body, RunJobRequest.JOB_ID_JSON_ATTRIBUTE)
        self.individuals = self._get_attribute(body, RunJobRequest.INDIVIDUALS_JSON_ATTRIBUTE)
        self.inputs = self._get_attribute(body, RunJobRequest.INPUTS_JSON_ATTRIBUTE)
        self.outputs = self._get_attribute(body, RunJobRequest.OUTPUTS_JSON_ATTRIBUTE)

    def _get_attribute(self, body, attribute_name, value_if_not_present=None):
        value = value_if_not_present
        if attribute_name in body:
            value = body[attribute_name]
        else:
            self.errors.append(f"No {attribute_name} specified")
        return value
