from django.test import TestCase

# Create your tests here.
from api.models import TrainingConfiguration


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
                training_configuration.created_on.isoformat().replace(
                    '00:00', '0000'
                ),
        })

    def get_training_configuration(self):
        return TrainingConfiguration.objects.create(
            algorithm='algo1.py',
            dockerfile='Dockerfile.dms',
        )