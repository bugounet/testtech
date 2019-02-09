import json
import os
from decimal import Decimal
from django.utils.timezone import now

from api.models import TrainingTask

from .base import BaseActionManager
from .abort_task import AbortTaskAction
from .build_task import BuildTaskAction
from .run_task import RunTaskAction
from .update_task_state import UpdateTaskStateAction


class TrainingTaskActionManager(BaseActionManager):
    """ Store tasks logics like getting docker elements IDs & tags,
    doing basic workflow operations
    """

    def __init__(self, model):
        super(BaseActionManager, self).__init__(model)
        self.configuration = model.training_configuration

    def mark_building(self):
        self.model.status = TrainingTask.BUILDING
        self.model.started_on = now()
        self.model.save(update_fields=['status', 'started_on'])

    def mark_training(self, docker_id):
        self.model.status = TrainingTask.TRAINING
        self.model.docker_id = docker_id
        self.model.save(update_fields=['status', 'docker_id'])

    def mark_failed(self, failure_message):
        self.model.failure_message = failure_message
        self.model.terminated_on = now()
        self.model.status = TrainingTask.FAILURE
        self.model.save(
            update_fields=['status', 'failure_message', 'terminated_on']
        )

    def mark_completed(self, test_loss, test_accuracy):
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
        return BuildTaskAction(self).run()

    def run(self, docker_client, docker_image):
        return RunTaskAction(self).run()

    def abort(self):
        return AbortTaskAction(self).run()

    def update_state(self, docker_client):
        return UpdateTaskStateAction(self).run()

    def get_working_dir(self):
        if not self.configuration.dockerfile:
            return None

        return os.path.dirname(
            os.path.realpath(
                self.configuration.dockerfile.path
            )
        )

    def get_dockerfile_name(self):
        if not self.configuration.dockerfile:
            return None
        return self.configuration.dockerfile.path.split(os.sep)[-1]

    def float_to_decimal(self, float_number):
        return Decimal(str(float_number))

    def get_image_tag(self):
        return "training:image{}".format(self.model.id)

    def get_container_name(self):
        return "training-container-{}".format(self.model.id)

    def get_results_output_dir(self):
        working_dir = self.get_working_dir()
        if working_dir is None:
            return None
        return os.sep.join(working_dir, "results-{}".format(self.model.id))

    def get_results_output(self):
        dir = self.get_results_output_dir()
        with open(os.sep.join(dir, 'score.json'), 'r') as f:
            return json.loads(f.read())
