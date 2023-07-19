import logging

try:
    import docker
    DOCKER_AVAILABLE = True
except ImportError:
    DOCKER_AVAILABLE = False


class DockerHelper:
    @staticmethod
    def get_image_id(image_name):
        if not DOCKER_AVAILABLE:
            return None
        
        try:
            client = docker.from_env()
            images = client.images.list()
            for image in images:
                for tag in image.tags:
                    if tag == image_name:
                        return image.id
            return None
        except docker.errors.DockerException as e:
            logging.exception("Failed to get Docker image ID: {}".format(str(e)))
            return None

    @staticmethod
    def get_current_image_name():
        if not DOCKER_AVAILABLE:
            return None

        try:
            container_id = open('/proc/self/cgroup').read().split('/')[-1].strip()
            client = docker.from_env()
            container_info = client.api.inspect_container(container_id)
            image_name = container_info['Config']['Image']
            return image_name
        except docker.errors.DockerException as e:
            logging.exception("Failed to get current Docker image name: {}".format(str(e)))
            return None

    @staticmethod
    def get_image_info():
        if not DOCKER_AVAILABLE:
            return None
        
        try:
            image_id = DockerHelper.get_image_id(DockerHelper.get_current_image_name())
            if not image_id:
                return None
            client = docker.from_env()
            image = client.images.get(image_id)
            return image.tags[0]
        except docker.errors.DockerException as e:
            logging.exception("Failed to retrieve Docker image info: {}".format(str(e)))
            return None
