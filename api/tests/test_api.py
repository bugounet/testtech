import datetime
from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase

# Create your tests here.
from pytz import utc

from api.models import TrainingConfiguration
from api.models import TrainingTask


def alter_tz_format(datetime_str):
    return datetime_str.replace("+00:00", "+0000")


class APITestCase(TestCase):
    def test_list_trainings(self):
        training_configuration = self.get_training_configuration()

        response = self.client.get("/api/trainings")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{
            "algorithm": 'algo1.py',
            "id": training_configuration.id,
            "dockerfile": 'Dockerfile.dms',
            "created_on":
                training_configuration.created_on.isoformat().replace(
                    '00:00', '0000'
                ),
        }])

    def test_get_single_training(self):
        training_configuration = self.get_training_configuration()

        response = self.client.get(
            "/api/training/{}".format(training_configuration.id)
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "algorithm": 'algo1.py',
            "id": training_configuration.id,
            "dockerfile": 'Dockerfile.dms',
            "created_on":
                alter_tz_format(training_configuration.created_on.isoformat())
        })

    def get_training_configuration(self):
        return TrainingConfiguration.objects.create(
            algorithm='algo1.py',
            dockerfile='Dockerfile.dms',
        )

    def test_get_tasks_list(self):
        training_configuration = self.get_training_configuration()

        task = TrainingTask.objects.create(
            training_configuration=training_configuration,
            status=TrainingTask.COMPLETE,
            failure_message="This is a test.",
            started_on=datetime.datetime(
                2019, 1, 16, 19, 15, 4, 1, tzinfo=utc
            ),
            terminated_on=datetime.datetime(
                2019, 1, 16, 19, 17, 23, 2, tzinfo=utc
            ),
            test_loss=Decimal("0.54231"),
            test_accuracy=Decimal("0.7462"),
        )

        response = self.client.get('/api/tasks')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{
            "training_configuration": training_configuration.pk,
            "status": TrainingTask.COMPLETE,
            "created_on": task.created_on.isoformat().replace(
                    '00:00', '0000'
                ),
            "started_on": alter_tz_format(task.started_on.isoformat()),
            "terminated_on": alter_tz_format(task.terminated_on.isoformat()),
            "id": task.id,
            "failure_message": "This is a test.",
            "test_loss": "0.542310", # Feature 6 decimals
            "test_accuracy": "0.746200", # Feature 6 decimals
        }])

    def test_get_task(self):
        training_configuration = self.get_training_configuration()

        task = TrainingTask.objects.create(
            training_configuration=training_configuration,
            status=TrainingTask.COMPLETE,
            failure_message="This is a test.",
            started_on=datetime.datetime(
                2019, 1, 16, 19, 15, 4, 1, tzinfo=utc
            ),
            terminated_on=datetime.datetime(
                2019, 1, 16, 19, 17, 23, 2, tzinfo=utc
            ),
            test_loss=Decimal("0.54231"),
            test_accuracy=Decimal("0.7462"),
        )

        response = self.client.get('/api/task/{}'.format(task.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "training_configuration": training_configuration.pk,
            "status": TrainingTask.COMPLETE,
            "created_on": task.created_on.isoformat().replace(
                    '00:00', '0000'
                ),
            "started_on": alter_tz_format(task.started_on.isoformat()),
            "terminated_on": alter_tz_format(task.terminated_on.isoformat()),
            "id": task.id,
            "failure_message": "This is a test.",
            "test_loss": "0.542310",
            "test_accuracy": "0.746200",
        })

    @patch('api.actions.TrainingConfigurationActionManager.run_training')
    def test_post_configuration_run(self, action_manager):
        training_configuration = self.get_training_configuration()
        task = self.get_memory_training_task()
        action_manager.return_value = task

        response = self.client.post('/api/training/{}/run/'.format(
            training_configuration.id
        ))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            "id": 2,
            "training_configuration": 1,
            "failure_response": None,
            "created_on":
                alter_tz_format(
                    datetime.datetime(2019, 1, 1, 0, 0, 0, tzinfo=utc)
                ),
            "started_on": None,
            "terminated_on": None,
            "test_loss": None,
            "test_accuracy": None,
            "status": TrainingTask.CREATED,
        })

    def get_memory_training_task(self):
        """ Return a non-saved model to avoid interactions with DB (faster
        test performances)
        """
        return TrainingTask(
            training_configuration_id=1,
            status=TrainingTask.CREATED,
            failure_message=None,
            started_on=None,
            terminated_on=None,
            test_loss=None,
            test_accuracy=None,
            id=2,
        )