# Imports
import logging
import zmq

from lib.models.run.run_job_request import RunJobRequest

#
# A ZMQ server class that handles polling for jobs.
#
class ZMQClient():
    #
    # Constructor.
    #
    def __init__(self, config):
        self.config = config
        self.context = zmq.Context()
        self._connect()

    #
    # Connects to the server.
    #
    def _connect(self):
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(self._generate_connection_string())

    #
    # Generates the connection string, using the config object.
    #
    def _generate_connection_string(self):
        return "tcp://localhost:5555"
    
    #
    # Polls for jobs
    #
    def poll_for_job(self):
        # Poller to check for incoming messages
        poller = zmq.Poller()
        poller.register(self.socket, zmq.POLLIN)

        self.socket.send(b"Hello")

        # Poll with a timeout (e.g., 5000 milliseconds = 5 seconds)
        events = dict(poller.poll(5000))

        if self.socket in events and events[self.socket] == zmq.POLLIN:
            # There is a message from the server
            json_data = self.socket.recv()
            return json_data
        
        return None
