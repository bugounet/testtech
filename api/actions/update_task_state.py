from logging import getLogger

import docker

from .base import SubActionManager
from api.models import TrainingTask

logger = getLogger(__name__)


class UpdateTaskStateAction(SubActionManager):
    def __init__(self, actions):
        self.actions = actions
        self.model = actions.model

    def run(self, docker_client=None):
        if docker_client is None:
            docker_client = docker.client.from_env()

        # If we have many self.model., the filtering might return self.model.
        # that have been aborted so update-status to make sure we're not
        # trying to get results from an aborted self.model.
        self.model.refresh_from_db(fields=['status'])
        if self.model.status != TrainingTask.TRAINING:
            logger.info(
                "Task {} is not running. skipped.".format(self.model.id)
            )
            return

        try:
            container = docker_client.containers.get(self.model.docker_id)
        except:

            logger.info("Docker looks offline. Retry later.")
            return

        # container status could be one of created, restarting, running,
        # removing, paused, exited, or dead
        if container.status in ('created', 'restarting', 'running'):
            logger.info(
                "Task {} is not terminated yet...".format(self.model.id)
            )
            return

        if container.status != 'exited':
            self.actions.mark_failed("Task crashed or got killed.")
            return

        # Try to get results
        try:
            output = self.actions.get_results_output()
        except Exception as e:
            self.actions.mark_failed(
                "Could not find task_results: {}".format(str(e))
            )
            return

        try:
            self.actions.mark_completed(
                # use decimals instead of floats for precision
                self.actions.float_to_decimal(output['test_loss']),
                self.actions.float_to_decimal(output['test_accuracy'])
            )
        except Exception as e:
            self.actions.mark_failed(
                "Could not parse task_results: {}".format(str(e))
            )
            return

        docker_client.containers.prune()
