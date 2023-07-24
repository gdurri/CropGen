import glob
import json
import logging
import logging.config
import os.path
import requests
import time

class LoggerConfig:

    def __init__(self, config):
        self.config = config
        self.this_script_path = os.path.dirname(__file__)
        self.log_directory = os.path.join(self.this_script_path, "..", "..", "logs")
        self.logger_config = "logger_config.ini"
        self.logging_config_path = os.path.join(self.this_script_path, self.logger_config)

    def _delete_all_log_files(self):
        if os.path.exists(self.log_directory):
            log_files = glob.glob(f'{self.log_directory}/*.log')
            for file in log_files:
                os.remove(file)

    def setup_logger(self):
        if self.config.delete_logs_on_startup:
            self._delete_all_log_files()

        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

        logging.config.fileConfig(self.logging_config_path)

        # Add the HTTPS handler
        self.add_https_handler()

        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)

    def add_https_handler(self):
        if not self.config.remote_logger_url:
            return

        # Set up the HTTPS handler manually
        handler = logging.StreamHandler()
        handler.emit = self.send_logs_to_server(self.config.remote_logger_url)

        self.json_formatter = JsonFormatter()  # Custom JSON formatter
        handler.setFormatter(self.json_formatter)

        # Add the handler to the root logger
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)

    def send_logs_to_server(self, url):
        def send_logs(record):
            try:
                headers = {'Content-type': 'application/json'}
                log_data = {
                    'file': record.filename,
                    'timestamp': self.json_formatter.formatTime(record),
                    'level': record.levelname,
                    'message': record.msg
                }
                response = requests.post(url=url, data=json.dumps(log_data, default=str), headers=headers)
                if response.status_code != 200:
                    logging.warning("Failed to send logs to the server. HTTP Status Code: %d", response.status_code)
            except Exception as ex:
                pass

        return send_logs


class JsonFormatter(logging.Formatter):
    """
    Custom JSON formatter that serializes the log record to JSON.
    """
    def format(self, record):
        log_data = {
            'file': record.filename,
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.msg
        }
        return json.dumps(log_data, default=str)

    def formatTime(self, record, datefmt=None):
        """
        Override the formatTime method to format the timestamp.
        """
        ct = self.converter(record.created)
        if datefmt:
            s = time.strftime(datefmt, ct)
        else:
            t = time.strftime("%Y-%m-%d %H:%M:%S", ct)
            s = "%s.%03d" % (t, record.msecs)
        return s

    def formatException(self, exc_info):
        if exc_info:
            return ''.join(logging._defaultFormatter.formatException(exc_info))
        return None
