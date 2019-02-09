from .base import BaseActionManager
from api.models import TrainingTask
from api.tasks import start_task


class TrainingConfigurationActionManager(BaseActionManager):
    """ Implement an "action manager" to group logic out of model class.
    The goal here is to make sure model only keeps data. It eases
    input mocking and ORM replacement if needed one day.
    """

    def run_training(self):
        task = TrainingTask.objects.create(
            training_configuration_id=self.model.pk,
        )
        start_task.delay(task.id)
        return task
