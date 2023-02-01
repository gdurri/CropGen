from enum import Enum

from lib.utils.date_time_helper import DateTimeHelper

# class syntax
class LogLevel(Enum):
    Trace = 1
    Debug = 2
    Info = 3
    Warn = 4
    Error = 5
    Fatal = 6


class Logger:
    # Constants
    TRACE_LOG_PREFIX = 'TRACE'
    DEBUG_LOG_PREFIX = 'DEBUG'
    INFO_LOG_PREFIX = 'INFO'
    WARN_LOG_PREFIX = 'WARN'
    ERROR_LOG_PREFIX = 'ERROR'
    FATAL_LOG_PREFIX = 'FATAL'

    def _log(self, log_level, log_entry):

        log_level_dictionary = {
            LogLevel.Trace: self._log_trace,
            LogLevel.Debug: self._log_debug,
            LogLevel.Info: self._log_info,
            LogLevel.Warn: self._log_warn,
            LogLevel.Error: self._log_error,
            LogLevel.Fatal: self._log_fatal
        }

        if log_level in log_level_dictionary.keys():
            log_level_dictionary[log_level](log_entry)

    def _log_trace(self, log_entry):
        self._print_log(self.TRACE_LOG_PREFIX, log_entry)

    def _log_debug(self, log_entry):
        self._print_log(self.DEBUG_LOG_PREFIX, log_entry)

    def _log_info(self, log_entry):
        self._print_log(self.INFO_LOG_PREFIX, log_entry)

    def _log_warn(self, log_entry):
        self._print_log(self.WARN_LOG_PREFIX, log_entry)

    def _log_error(self, log_entry):
        print("{} - {}".format(self.ERROR_LOG_PREFIX, log_entry))

    def _log_fatal(self, log_entry):
        self._print_log(self.FATAL_LOG_PREFIX, log_entry)

    def _print_log(self, log_prefix, log_entry):
        date_str = DateTimeHelper._get_date_time_now_str()
        print(f"{date_str}: {log_prefix} - {log_entry}")
