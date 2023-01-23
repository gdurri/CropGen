class RunJobRequest:
  # Constants
  JOB_ID_JSON_ATTRIBUTE = 'jobId'

  def __init__(self, logger, request_data):
    self.logger = logger
    self.errors = []
    self._parse(request_data)

  def _parse(self, request_data):

    self.valid = True
    self.job_id = request_data.json.get(self.JOB_ID_JSON_ATTRIBUTE, None)

    if self.job_id == None:
        self.valid = False
        job_id_missing_error = f"No {self.JOB_ID_JSON_ATTRIBUTE} specified"
        self.errors.append(job_id_missing_error)
        self.logger._log_warn(job_id_missing_error)
