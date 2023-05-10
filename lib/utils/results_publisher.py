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
        config
    ):
        self.iteration_results_url = iteration_results_url
        self.final_results_url = final_results_url
        self.config = config

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
        logging.debug("Results: '%s'", results.to_json(self.config.pretty_print_json_in_logs))

        try:
            response = requests.put(
                headers={'Content-type': 'application/json'},
                url=url, 
                data=json,
                timeout=self.config.results_publisher_timeout_seconds
            )
        except Exception:
            logging.exception(f"Failed to publish results to {url}")
            return None
        
        if response.ok:
            logging.info("Successfully published results to: '%s'", url)
        else:
            logging.error("Failed to publish results to: '%s'. Reason: '%s'", url, response.reason)

        return response
