from uuid import uuid4

from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin
)
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from api.actions import TrainingConfigurationActionManager
from api.exceptions import IncompleteConfiguration
from api.models import TrainingConfiguration
from api.serializers import TrainingConfigurationSerializer


class GenericTrainingView(GenericAPIView):
    serializer_class = TrainingConfigurationSerializer
    queryset = TrainingConfiguration.objects.all()


class TrainingConfigurationListView(CreateModelMixin, ListModelMixin,
                                    GenericTrainingView):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TrainingConfigurationDetailView(RetrieveModelMixin, GenericTrainingView):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class TrainingConfigurationRunActionView(GenericTrainingView):

    def post(self, request, *args, **kwargs):
        """ Schedules a training task for this configuration
        """
        training_configuration = self.get_object()
        actions = TrainingConfigurationActionManager(training_configuration)
        try:
            task = actions.run_training()
        except IncompleteConfiguration as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'id': task.id},
            status=status.HTTP_201_CREATED
        )
