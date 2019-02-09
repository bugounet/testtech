""" Celery tasks file. Celery will run python scripts in background for us.
The goal here is not to lock API when it requests a Training to be
done because building the image, and then runing the container
will be very long & slow.
So the API will trig a celery-task. The task will then fetch TrainingTask &
config to update them as the job goes."""
from logging import getLogger

import docker

from test_owkin import celery_app

logger = getLogger(__name__)


@celery_app.task
def start_task(task_id):
    from api.actions import TrainingTaskActionManager
    from api.models import TrainingTask
    # Retreive essential models
    try:
        task = TrainingTask.objects.get(pk=task_id)
    except TrainingTask.DoesNotExist:
        print("Task has been removed before build process start. Aborting.")
        return

    try:
        docker_client = docker.from_env()
    except:
        print("Client looks down. Try again later.")
        #  could do better with a "task.fail" after N postpones
        start_task.delay(countdown=30)
        return

    actions = TrainingTaskActionManager(task)

    docker_image = actions.build(docker_client)
    if docker_image:
        actions.run(docker_client, docker_image)


@celery_app.task
def check_results():
    from api.actions import TrainingTaskActionManager
    from api.models import TrainingTask

    try:
        docker_client = docker.from_env()
    except:
        print("Client looks down. Try again later.")
        return

    for task in TrainingTask.objects.training():
        TrainingTaskActionManager(task).update_state(docker_client)
