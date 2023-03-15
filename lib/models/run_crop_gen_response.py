from lib.models.model import Model

#
# The Run response message. Used to signal that a run has started and whether it is successful.
#
class RunCropGenResponse(Model):
    #
    # Constructor
    #
    def __init__(self, job_id, successful, errors):
        self.JobID = job_id
        self.Successful = successful
        self.Errors = errors

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__
