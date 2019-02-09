from logging import getLogger

import docker

from .base import SubActionManager
logger = getLogger(__name__)

class BuildTaskAction(SubActionManager):
    def __init__(self, actions):
        self.actions = actions
        self.model = actions.model

    def run(self, docker_client=None):
        if docker_client is None:
            docker_client = docker.client.from_env()

        self.actions.mark_building()

        working_dir = self.actions.get_working_dir()
        dockerfile_name = self.actions.get_dockerfile_name()

        try:
            logger.info(
                'Calling docker: %s %s %s',
                self.actions.get_image_tag(),
                working_dir,
                dockerfile_name
            )
            image, _ = docker_client.images.build(
                tag=self.actions.get_image_tag(),
                path=working_dir,
                dockerfile=dockerfile_name
            )
            return image
        except Exception as e:
            self.actions.mark_failed(
                "Failed to start image build: {}".format(str(e))
            )
            return None
