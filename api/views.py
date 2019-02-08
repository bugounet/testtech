from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin

from api.models import TrainingConfiguration
from api.serializers import TrainingConfigurationSerializer


class TrainingConfigurationListView(ListModelMixin, GenericAPIView):
    queryset = TrainingConfiguration.objects.all()
    serializer_class = TrainingConfigurationSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
