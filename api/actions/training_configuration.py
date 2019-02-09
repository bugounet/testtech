from api.exceptions import IncompleteConfiguration
from .base import BaseActionManager
from api.models import TrainingTask
from api.tasks import start_task
from django.utils.translation import ugettext_lazy as _


class TrainingConfigurationActionManager(BaseActionManager):
    """ Implement an "action manager" to group logic out of model class.
    The goal here is to make sure model only keeps data. It eases
    input mocking and ORM replacement if needed one day.
    """

    def run_training(self):
        if not self.model.algorithm or not self.model.dockerfile:
            raise IncompleteConfiguration(
                _("Make sure docker file and algorithm are set.")
            )

        task = TrainingTask.objects.create(
            training_configuration_id=self.model.pk,
        )
        start_task.delay(task.id)
        return task
