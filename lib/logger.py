from enum import Enum
from datetime import date

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

  def _log(self, log_evel, log_entry):
    if log_evel == LogLevel.Trace:
      self._log_trace(log_entry)
    elif log_evel == LogLevel.Debug:
      self._log_debug(log_entry)
    elif log_evel == LogLevel.Info:
      self._log_info(log_entry)
    elif log_evel == LogLevel.Warn:
      self._log_warn(log_entry)
    elif log_evel == LogLevel.Error:
      self._log_error(log_entry)
    elif log_evel == LogLevel.Fatal:
      self._log_fatal(log_entry)

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
    print("{}: {} - {}".format, (date.today(), log_prefix, log_entry))
