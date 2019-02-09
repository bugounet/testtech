import docker

from .base import SubActionManager
from api.models import TrainingTask


class RunTaskAction(SubActionManager):
    def __init__(self, actions):
        self.actions = actions
        self.model = actions.model

    def run(self, docker_client, docker_image):
        if docker_client is None:
            docker_client = docker.client.from_env()
        self.model.status = TrainingTask.TRAINING
        self.model.save(update_fields=['status'])

        try:
            container = docker_client.containers.run(
                docker_image,
                "-V /training_output/",
                volumes={
                    self.actions.get_working_dir(): {
                        'bind': '/training_output', 'mode': 'rw'
                    }
                },
                detach=True,
                name=self.actions.get_container_name()
            )
        except Exception as e:
            self.actions.mark_failed(
                "Failed to run docker container : {}".format(str(e))
            )
            return None

        self.actions.mark_training(container.id)
        return container
