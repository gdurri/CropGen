from lib.models.model import Model

#
# A message wrapper
#
class MessageWrapper(Model):
    #
    # Constructor
    #
    def __init__(self, type_name, type_body):
        self.TypeName = type_name
        self.TypeBody = type_body

    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__