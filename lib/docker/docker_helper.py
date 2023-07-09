import docker
import logging

#
# A Docker helper class
#
class DockerHelper():
    #
    # Gets the image id for the current container.
    #
    @staticmethod
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
        container_id = open('/proc/self/cgroup').read().split('/')[-1].strip()
        client = docker.from_env()
        container_info = client.api.inspect_container(container_id)
        image_name = container_info['Config']['Image']
        return image_name

    #
    # Gets the image info of the container that we are running in.
    #
    @staticmethod
    def get_image_info():
        try:
            image_id = DockerHelper.get_image_id(DockerHelper.get_current_image_name())
            if not image_id:
                return None
            client = docker.from_env()
            image = client.images.get(image_id)
            return image.tags[0]
        except docker.errors.DockerException as e:
            logging.exception("Failed to retrieve Docker Image Info: {}".format(str(e)))
            return None
