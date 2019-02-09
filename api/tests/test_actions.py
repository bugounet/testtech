import datetime
import time
from decimal import Decimal
from unittest.mock import Mock

from django.test import TestCase
from django.utils.timezone import now

from pytz import utc

from api.actions import TrainingConfigurationActionManager
from api.actions import TrainingTaskActionManager
from api.models import TrainingConfiguration
from api.models import TrainingTask


def alter_tz_format(datetime_str):
    return datetime_str.replace("+00:00", "+0000")


def to_timestamp(date_time_instance):
    return time.mktime(date_time_instance.timetuple())


class ActionManagersTestCase(TestCase):

    def test_schedule_training_task(self):
        training_configuration = self.get_training_configuration()
        actions = TrainingConfigurationActionManager(
            training_configuration
        )

        task = actions.run_training()

        self.assertEqual(task.training_configuration, training_configuration)
        self.assertEqual(task.status, TrainingTask.CREATED)
        self.assertEqual(task.started_on, None)
        self.assertEqual(task.terminated_on, None)
        self.assertEqual(task.test_loss, None)
        self.assertEqual(task.test_accuracy, None)
        self.assertAlmostEqual(
            to_timestamp(task.created_on),
            to_timestamp(datetime.datetime.now())
        )

    def get_training_configuration(self):
        return TrainingConfiguration.objects.create(
            algorithm='algo1.py',
            dockerfile='Dockerfile.dms',
        )
    def get_training_task(self, status=TrainingTask.CREATED):
        started_on = now() if status != TrainingTask.CREATED else None
        return TrainingTask.objects.create(
            training_configuration=self.get_training_configuration(),
            status=status,
            started_on=started_on
        )

    def test_build_action_success(self):
        task = self.get_training_task()
        image = Mock()
        mocked_client = Mock()
        mocked_client.images.build.return_value = (image, [])
        actions = TrainingTaskActionManager(task)

        result = actions.build(
            docker_client=mocked_client
        )

        self.assertEqual(actions.model.status, TrainingTask.BUILDING)
        self.assertNotEqual(actions.model.started_on, None)
        self.assertTrue(mocked_client.images.build.called)
        self.assertEqual(result, image)

    def test_build_action_failure(self):
        task = self.get_training_task()
        mocked_client = Mock()
        mocked_client.images.build.side_effect = Exception("Oops")
        actions = TrainingTaskActionManager(task)

        actions.build(
            docker_client=mocked_client
        )

        self.assertEqual(actions.model.status, TrainingTask.FAILURE)
        self.assertEqual(
            actions.model.failure_message,
            "Failed to start image build: Oops"
        )
        self.assertNotEqual(actions.model.started_on, None)
        self.assertTrue(mocked_client.images.build.called)

    def test_build_action_failure(self):
        task = self.get_training_task()
        mocked_client = Mock()
        mocked_client.images.build.side_effect = Exception("Oops")
        actions = TrainingTaskActionManager(task)

        actions.build(
            docker_client=mocked_client
        )

        self.assertEqual(actions.model.status, TrainingTask.FAILURE)
        self.assertEqual(
            actions.model.failure_message,
            "Failed to start image build: Oops"
        )
        self.assertNotEqual(actions.model.started_on, None)
        self.assertTrue(mocked_client.images.build.called)

    def test_run_action_failure(self):
        task = self.get_training_task(status=TrainingTask.BUILDING)
        image = Mock()
        mocked_client = Mock()
        mocked_client.containers.run.side_effect = Exception("Oops")
        actions = TrainingTaskActionManager(task)

        result = actions.run(
            docker_client=mocked_client, docker_image=image
        )

        self.assertEqual(actions.model.status, TrainingTask.FAILURE)
        self.assertEqual(
            actions.model.failure_message,
            "Failed to run docker container : Oops"
        )
        self.assertNotEqual(actions.model.started_on, None)
        self.assertTrue(mocked_client.containers.run.called)
        self.assertEqual(result, None)

    def test_run_action_success(self):
        task = self.get_training_task(status=TrainingTask.BUILDING)
        container = Mock(id=2345)
        image = Mock()
        mocked_client = Mock()
        mocked_client.containers.run.return_value = container
        actions = TrainingTaskActionManager(task)

        result = actions.run(
            docker_client=mocked_client, docker_image=image
        )

        self.assertEqual(actions.model.status, TrainingTask.TRAINING)
        self.assertEqual(actions.model.failure_message, None)
        self.assertTrue(mocked_client.containers.run.called)
        self.assertEqual(result, container)
