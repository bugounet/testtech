from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from api.models import TrainingConfiguration
from api.serializers import TrainingConfigurationSerializer


class GenericTrainingView(GenericAPIView):
    queryset = TrainingConfiguration.objects.all()


class TrainingConfigurationListView(ListModelMixin, GenericTrainingView):
    serializer_class = TrainingConfigurationSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TrainingConfigurationDetailView(RetrieveModelMixin, GenericTrainingView):
    serializer_class = TrainingConfigurationSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
