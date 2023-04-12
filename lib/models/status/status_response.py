from lib.models.common.model import Model

#
# End of run message for signalling that a run has completed.
#
class StatusResponse(Model):
    #
    # Constructor
    #
    def __init__(self, running_job):
        self.IsRunningJob = running_job != ''
        self.RunningJob = running_job

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__
