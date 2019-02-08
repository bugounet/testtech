import datetime
import time
from decimal import Decimal
from django.test import TestCase

from pytz import utc

from api.actions import TrainingConfigurationActionManager
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
