from django.test import SimpleTestCase

# Create your tests here.
class APITestCase(SimpleTestCase):
    def test_list_trainings(self):
        response = self.client.get("/api/trainings")

        self.assertJSONEqual(response, [{
            "algorithm": 'algo1.py',
            "id": "1",
            "dockerfile": 'Dockerfile.dms',
            "created_on": '2019-01-01T00:00:00',
        }])
