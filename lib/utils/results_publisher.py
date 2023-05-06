import logging
import requests

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
        json = results.to_json()
        logging.info("Publishing results to: '%s'", url)
        logging.debug("Results: '%s'", results.to_json(True))

        try:
            response = requests.put(
                headers={'Content-type': 'application/json'},
                url=url, 
                data=json,
                timeout=self.timeout
            )
        except Exception:
            logging.exception("Failed to publish results")
            return None
        
        if response.ok:
            logging.info("Successfully published results to: '%s'", url)
        else:
            logging.error("Failed to publish results to: '%s'. Reason: '%s'", url, response.reason)

        return response
