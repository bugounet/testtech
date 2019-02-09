import json
import os
from logging import getLogger

from decimal import Decimal
from django.utils.timezone import now
from api.tasks import start_task
from api.models import TrainingTask

logger = getLogger(__name__)


class TrainingConfigurationActionManager(object):
    """ Implement an "action manager" to group logic out of model class.
    The goal here is to make sure model only keeps data. It eases
    input mocking and ORM replacement if needed one day.
    """
    def __init__(self, configuration):
        self.model = configuration

    def run_training(self):
        task = TrainingTask.objects.create(
            training_configuration_id=self.model.pk,
        )
        start_task.delay(task.id)
        return task



class TrainingTaskActionManager(object):
    """ Store task logics like getting docker elements IDs & tags.
    """

    def __init__(self, task):
        self.model = task
        self.configuration = task.training_configuration

    def mark_task_failure(self, failure_message):
        self.model.failure_message = failure_message
        self.model.terminated_on = now()
        self.model.status = TrainingTask.FAILURE
        self.model.save(
            update_fields=['status', 'failure_message', 'terminated_on']
        )

    def mark_task_completion(self, test_loss, test_accuracy):
        self.model.test_loss = test_loss
        self.model.test_accuracy = test_accuracy
        self.model.terminated_on = now()
        self.model.status = TrainingTask.COMPLETE
        self.model.save(
            update_fields=[
                'status', 'terminated_on', 'test_loss', 'test_accuracy'
            ]
        )

    def build(self, docker_client):
        self.model.status = TrainingTask.BUILDING
        self.model.started_on = now()
        self.model.save(update_fields=['status', 'started_on'])

        working_dir = self._get_working_dir()
        dockerfile_name = self._get_dockerfile_name()

        try:
            image, _ = docker_client.images.build(
                tag=self._get_image_tag(),
                path=working_dir,
                dockerfile=dockerfile_name
            )
            return image
        except Exception as e:
            self.mark_task_failure(
                "Failed to start image build: {}".format(str(e))
            )
            return None

    def run(self, docker_client, docker_image):
        self.model.status = TrainingTask.TRAINING
        self.model.save(update_fields=['status'])


        container = docker_client.containers.run(
            docker_image,
            "-V /training_output/",
            volumes={
                self._get_working_dir(): {
                    'bind': '/training_output', 'mode': 'rw'
                }
            },
            detach=True,
            name=self._get_container_name()
        )

        self.model.status = TrainingTask.TRAINING
        self.model.docker_id = container.id
        self.model.save(update_fields=['status', 'docker_id'])

    def update_state(self, docker_client):
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
            self.mark_task_failure("Task crashed or got killed.")
            return

        # Try to get results
        try:
            output = self._get_results_output()
        except Exception as e:
            self.mark_task_failure(
                "Could not find self.model.results: {}".format(str(e))
            )
            return

        try:
            self.mark_task_completion(
                # use decimals instead of floats for precision
                self._float_to_decimal(output['test_loss']),
                self._float_to_decimal(output['test_accuracy'])
            )
        except Exception as e:
            self.mark_task_failure(
                "Could not parse self.model.results: {}".format(str(e))
            )
            return

    def _get_working_dir(self):
        if not self.configuration.dockerfile:
            return None

        return os.path.dirname(
            os.path.realpath(
                self.configuration.dockerfile.path
            )
        )

    def _get_dockerfile_name(self):
        if not self.configuration.dockerfile:
            return None
        return self.configuration.dockerfile.path.split(os.sep)[-1]

    def _float_to_decimal(self, float_number):
        return Decimal(str(float_number))

    def _get_image_tag(self):
        return "training:image{}".format(self.model.id)

    def _get_container_name(self):
        return "training-container-{}".format(self.model.id)

    def _get_results_output_dir(self):
        working_dir = self._get_working_dir()
        if working_dir is None:
            return None
        return os.sep.join(working_dir, "results-{}".format(self.model.id))

    def _get_results_output(self):
        dir = self._get_results_output_dir()
        with open(os.sep.join(dir, 'score.json'), 'r') as f:
            return json.loads(f.read())
