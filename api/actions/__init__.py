from api.models import TrainingTask


class TrainingConfigurationActionManager(object):
    """ Implement an "action manager" to group logic out of model class.
    The goal here is to make sure model only keeps data. It eases
    input mocking and ORM replacement if needed one day.
    """
    def __init__(self, action):
        self.model = action

    def run_training(self):
        return TrainingTask.objects.create(
            training_configuration_id=self.model.pk,
        )
