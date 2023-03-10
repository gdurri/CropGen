import logging
import requests

#
# A class that is responsible for publishing the "Problem" results.
#
class ResultsPublisher():
    #
    # Constructor
    #    
    def __init__(self, url):
        self.url = url

    #
    # Convert and publish the results.
    #
    def publish_results(self, results):
        data = results.to_json()

        logging.info("Publishing results to: '%s'", self.url)
        logging.debug("Results: '%s'", data)

        response = requests.post(
            url=self.url, 
            data=data
        )

        if not response.ok:
            logging.error("Failed to publish results to: '%s'. Reason: '%s'", self.url, response.reason)
        else:
            logging.info("Successfully published results to: '%s'", self.url)

        return response