import logging

from lib.utils.constants import Constants
from lib.socket.socket_client import SocketClient
from lib.socket.socket_client_base import ReadMessageData
from lib.utils.date_time_helper import DateTimeHelper

#
# The real CGM Client
#
class CGMClient:

    #
    # Constructor
    #
    def __init__(self, host, port, config):
        self.host = host
        self.port = port
        self.config = config

    #
    # Tests whether we can connect to the CGM server over our socket.
    #
    def test_cgm_connection(self):
        try:
            logging.info("Testing CGM Connection")
            socket_client = SocketClient(self.config)
            socket_client.set_timeout(self.config.socket_timeout_test_connection_seconds)
            socket_client.connect(self.host, self.port)
        except Exception:
            logging.error("CGM Connection NOT OK")
            return False
        logging.info("CGM Connection OK")
        return True
    
    #
    # Handles constructing a new socket connection to the CGM, sending the
    # message and returning the raw response.
    #
    def call_cgm(self, message):
        errors = []
        try:
            logging.info("Calling CGM with message: '%s'", message.get_type_name())
            logging.debug("Message data: %s", message.to_json(self.config.pretty_print_json_in_logs))

            request_start_time = DateTimeHelper.get_date_time()
            socket_client = SocketClient(self.config)
            socket_client.connect(self.host, self.port)
            socket_client.write_text(message)
            socket_client.set_timeout(self.config.socket_timeout_seconds)
            data =  socket_client.read_text()
            logging.debug("Received response from: %s request. Time taken: %s", message.get_type_name(), DateTimeHelper.get_elapsed_time_since(request_start_time))
            return data
        except Exception as exception:
            error = f"{Constants.CGM_SERVER_EXCEPTION} ({self.host}:{self.port}) - {exception}"
            logging.error(error)
            errors.append(error)

        return ReadMessageData(errors, None)
    
    #
    # Validates the read message data and captures all of the errors. 
    # If this returns true, the object is safe to use.
    #
    def validate_cgm_call(self, read_message_data):
        if not read_message_data:
            return [Constants.CGM_SERVER_NO_DATA_READ]

        # This is to handle any exceptions thrown from the Python code.
        if read_message_data.errors:
            return read_message_data.errors
        
        if not read_message_data.message_wrapper or \
           not read_message_data.message_wrapper.TypeName or \
           not read_message_data.message_wrapper.TypeBody:
            return [Constants.CGM_SERVER_INVALID_RESPONSE]

        # This is to handle an error response.
        if read_message_data.message_wrapper.TypeName == Constants.CGM_SERVER_TYPE_NAME_EXCEPTION_RESPONSE:
            return [f'{Constants.CGM_SERVER_ERROR_RESPONSE}: {read_message_data.message_wrapper.TypeBody}']
        
        return []
