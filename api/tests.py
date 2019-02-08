from django.test import TestCase

# Create your tests here.
from api.models import TrainingConfiguration


class APITestCase(TestCase):
    def test_list_trainings(self):
        training_configuration = TrainingConfiguration.objects.create(
            algorithm='algo1.py',
            dockerfile='Dockerfile.dms',
        )
        response = self.client.get("/api/trainings")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{
            "algorithm": 'algo1.py',
            "id": training_configuration.id,
            "dockerfile": 'Dockerfile.dms',
            "created_on": training_configuration.created_on.isoformat(),
        }])
