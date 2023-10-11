import os
import sys
import psutil
import logging
import docker

#
# A helper class for restarting this application.
#
class Restart():
    
    #
    # Restarts this program.
    #
    @staticmethod
    def perform_restart(is_running_in_docker):
        try:
            if is_running_in_docker:
                Restart.perform_restart_docker()
            else:
                Restart.perform_restart()
        except Exception:
            logging.exception("Failed to restart program")

    #
    # Restarts this program when running in docker.
    #
    @staticmethod
    def perform_restart_docker():
        logging.warn("perform_restart_docker is not implemented!")
        # docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        # docker_client.containers.get("cropgen").restart()

    #
    # Restarts this program, when not running in docker.
    #
    @staticmethod
    def perform_restart(is_running_in_docker):
        # python = sys.executable
        # # Use sys.argv to pass the original command-line arguments
        # os.execv(python, [python] + sys.argv)
        logging.warn("perform_restart is not implemented!")