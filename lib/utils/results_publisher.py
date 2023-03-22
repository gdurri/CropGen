import logging
import requests

from lib.models.message_wrapper import MessageWrapper

#
# A class that is responsible for publishing the "Problem" results.
#
class ResultsPublisher():
    #
    # Constructor
    #    
    def __init__(
        self, 
        iteration_results_url,
        final_results_url, 
        timeout
    ):
        self.iteration_results_url = iteration_results_url
        self.final_results_url = final_results_url
        self.timeout = timeout

    #
    # Publish the iteration results.
    #
    def publish_iteration_results(self, results):
        return self._publish_results(self.iteration_results_url, results)
    
    #
    # Publish the final results.
    #
    def publish_final_results(self, results):
        return self._publish_results(self.final_results_url, results)

    #
    # Publish the results.
    #
    def _publish_results(self, url, results):
        data = self._prepare_data_for_publish(results)

        logging.info("Publishing results to: '%s'", url)
        logging.debug("Results: '%s'", data)

        try:
            response = requests.put(
                headers={
                    'Content-type': 'application/json'
                },
                url=url, 
                data=data,
                timeout=self.timeout,
                
            )
        except Exception:
            logging.exception("Failed to publish results")
            return None
        
        if not response.ok:
            logging.error("Failed to publish results to: '%s'. Reason: '%s'", url, response.reason)
        else:
            logging.info("Successfully published results to: '%s'", url)

        return response
    
    #
    # Prepares data ready to publish
    #
    def _prepare_data_for_publish(self, message):
        message_wrapper = MessageWrapper()
        message_wrapper.set_type_name(message.get_type_name())
        message_wrapper.set_type_body(message.to_json())
        data = message_wrapper.to_json()
        return data