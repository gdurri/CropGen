from test.test_base import TestBase

class TestAggregateFunction(TestBase):
    def __init__(self, values):
        self.values = values
    
    def get_param_by_index(self, index):
        param = None
        if len(self.values) > index:
            return self.values[index]
        else:
            super().log_to_console(f"TestAggregateFunction: No value at index: {index}")
        return param