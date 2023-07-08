import subprocess
import json
import docker
import logging

#
# A Docker helper class
#
class DockerHelper():
    #
    # Gets the image id for the current container.
    #
    def get_image_id(image_name):
        client = docker.from_env()
        images = client.images.list()
        for image in images:
            for tag in image.tags:
                if tag == image_name:
                    return image.id
        return None
    
    #
    # Gets the current docker image name.
    #
    @staticmethod
    def get_current_image_name():
        container_id = subprocess.check_output(['cat', '/proc/self/cgroup']).decode('utf-8').strip().split('/')[-1]
        inspect_output = subprocess.check_output(['docker', 'inspect', container_id]).decode('utf-8')
        container_info = json.loads(inspect_output)
        image_name = container_info[0]['Config']['Image']
        return image_name

    #
    # Gets the image info of the container that we are running in.
    #
    @staticmethod
    def get_image_info():
        try:
            image_id = DockerHelper.get_image_id(DockerHelper.get_current_image_name())
            if not image_id: return None
            client = docker.from_env()
            image = client.images.get(image_id)
            return image.tags[0]
        except:
            logging.exception("Failed to retrieve Docker Image Info.")
            return None
