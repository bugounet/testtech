from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import TrainingConfiguration


class TrainingConfigurationListView(APIView):
    def get(self, request, *args, **kwargs):
        return Response([
            {
                'algorithm': training_configuration.algorithm.name,
                'dockerfile': training_configuration.dockerfile.name,
                'id': training_configuration.id,
                'created_on': training_configuration.created_on.isoformat()
            }
            for training_configuration in TrainingConfiguration.objects.all()
        ])
