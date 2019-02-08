from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin

from api.models import TrainingTask
from api.serializers import TrainingTaskSerializer


class GenericTrainingTaskView(GenericAPIView):
    queryset = TrainingTask.objects.all()


class TrainingTaskListView(ListModelMixin, GenericTrainingTaskView):
    serializer_class = TrainingTaskSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
