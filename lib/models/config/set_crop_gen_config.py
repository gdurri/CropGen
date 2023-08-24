import json
import logging

from lib.models.common.model import Model
from lib.utils.json_helper import JsonHelper

#
# Model that represents a set cropgen config request sent from the jobs server
#
class SetCropGenConfig(Model):
    #
    # Constructor.
    #
    def __init__(self):
        self.ApsimClockDateFormat = '',
        self.ApsimClockEndDateYearInputName = '',
        self.ApsimClockStartDateYearInputName = ''
        self.ApsimSimulationEndDateAddYear = 0
        self.ApsimSimulationStartDate = ''
        self.ApsimSimulationStartDateAddYear = 0
        self.MinimumRequiredCGMWorkers = 0
        self.PrettyPrintJsonInLogs = False
        self.PublishResults = True
        self.RemoteLoggerUrl = ''
        self.ResultsPublisherTimeoutSeconds = 0
        self.RoundUpYearsInMeanCalculation = True
        self.SocketTimeoutSeconds = 0
        self.SocketTimeoutTestConnectionSeconds = 0

    #
    # Parses the JSON data into this class.
    #
    def parse_from_json_string(self, message):
        try:
            json_object = json.loads(message)
            self.ApsimClockDateFormat = JsonHelper.get_non_mandatory_attribute(json_object, 'ApsimClockDateFormat', None)
            self.ApsimClockEndDateYearInputName = JsonHelper.get_non_mandatory_attribute(json_object, 'ApsimClockEndDateYearInputName', None)
            self.ApsimClockStartDateYearInputName = JsonHelper.get_non_mandatory_attribute(json_object, 'ApsimClockStartDateYearInputName', None)
            self.ApsimSimulationEndDateAddYear = JsonHelper.get_non_mandatory_attribute(json_object, 'ApsimSimulationEndDateAddYear', None)
            self.ApsimSimulationStartDate = JsonHelper.get_non_mandatory_attribute(json_object, 'ApsimSimulationStartDate', None)
            self.ApsimSimulationStartDateAddYear = JsonHelper.get_non_mandatory_attribute(json_object, 'ApsimSimulationStartDateAddYear', None)
            self.MinimumRequiredCGMWorkers = JsonHelper.get_non_mandatory_attribute(json_object, 'MinimumRequiredCGMWorkers', None)
            self.PrettyPrintJsonInLogs = JsonHelper.get_non_mandatory_attribute(json_object, 'PrettyPrintJsonInLogs', None)
            self.PublishResults = JsonHelper.get_non_mandatory_attribute(json_object, 'PublishResults', None)
            self.RemoteLoggerUrl = JsonHelper.get_non_mandatory_attribute(json_object, 'RemoteLoggerUrl', None)
            self.ResultsPublisherTimeoutSeconds = JsonHelper.get_non_mandatory_attribute(json_object, 'ResultsPublisherTimeoutSeconds', None)
            self.RoundUpYearsInMeanCalculation = JsonHelper.get_non_mandatory_attribute(json_object, 'RoundUpYearsInMeanCalculation', None)
            self.SocketTimeoutSeconds = JsonHelper.get_non_mandatory_attribute(json_object, 'SocketTimeoutSeconds', None)
            self.SocketTimeoutTestConnectionSeconds = JsonHelper.get_non_mandatory_attribute(json_object, 'SocketTimeoutTestConnectionSeconds', None)
            
        except Exception as error:
            logging.error(f"Failed to parse {self.get_type_name()} JSON: '{message}'. Error: '{error}'")
    
    #
    # Returns the type name.
    #
    def get_type_name(self):
        return __class__.__name__
