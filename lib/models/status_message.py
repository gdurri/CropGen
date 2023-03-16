from lib.models.model import Model

#
# End of run message for signalling that a run has completed.
#
class StatusMessage(Model):
    #
    # Constructor
    #
    def __init__(self, running_job):
        self.IsRunningJob = running_job != None
        self.RunningJob = running_job if running_job else 0

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__
