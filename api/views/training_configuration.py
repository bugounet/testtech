from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from api.models import TrainingConfiguration
from api.serializers import TrainingConfigurationSerializer


class TrainingConfigurationListView(ListModelMixin, GenericAPIView):
    queryset = TrainingConfiguration.objects.all()
    serializer_class = TrainingConfigurationSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TrainingConfigurationDetailView(RetrieveModelMixin, GenericAPIView):
    queryset = TrainingConfiguration.objects.all()
    serializer_class = TrainingConfigurationSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
