import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class TrainingConfigurationListView(APIView):
    def get(self, request, *args, **kwargs):
        return Response([
            {
                'algorithm': 'algo1.py',
                'dockerfile': 'Dockerfile.dms',
                'id': '1',
                'created_on': '2019-01-01T00:00:00'
            }
        ])
