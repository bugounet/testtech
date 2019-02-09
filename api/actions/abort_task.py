import docker

from api.exceptions import AbortFailed, AbortNotPossible
from api.models import TrainingTask


class AbortTaskAction(object):
    def __init__(self, actions):
        self.actions = actions
        self.model = actions.model

    def run(self):
        if self.model.status in (TrainingTask.CREATED, TrainingTask.BUILDING):
            self.model.status = TrainingTask.ABORTED
            self.model.save(update_fields=['status'])
            return

        if self.model.status == TrainingTask.TRAINING:
            docker_client = docker.client.from_env()
            try:
                container = docker_client.containers.get(self.model.docker_id)
            except Exception:
                raise AbortFailed('Docker container not found')

            if container.status not in ('created', 'restarting', 'running'):
                return

            try:
                container.kill()
            except Exception as e:
                raise AbortFailed(
                    'Docker refused to kill task: {}'.format(str(e))
                )
            else:
                return

        if self.model.status in (TrainingTask.FAILURE, TrainingTask.COMPLETE):
            raise AbortNotPossible("Current status does not allow it.")
