import logging
import requests

#
# A class that is responsible for publishing the "Problem" results.
#
class ResultsPublisher():
    #
    # Constructor
    #    
    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout

    #
    # Convert and publish the results.
    #
    def publish_results(self, results):
        data = results.to_json()

        logging.info("Publishing results to: '%s'", self.url)
        logging.debug("Results: '%s'", data)

        try:
            response = requests.post(
                url=self.url, 
                data=data,
                timeout=self.timeout
            )
        except Exception:
            logging.exception("Failed to publish results")
            return None
        
        if not response.ok:
            logging.error("Failed to publish results to: '%s'. Reason: '%s'", self.url, response.reason)
        else:
            logging.info("Successfully published results to: '%s'", self.url)

        return response