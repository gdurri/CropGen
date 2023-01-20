class RunJobRequest:
  def __init__(self, request_data):
    self.errors = []
    self._parse(request_data)

  def _parse(self, request_data):

    self.valid = True
    self.job_id = request_data.json.get('jobId', None)

    if self.job_id == None:
        self.valid = False
        self.errors.append("No jobId specified")
