from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from api.models import TrainingTask
from api.serializers import TrainingTaskSerializer


class GenericTrainingTaskView(GenericAPIView):
    serializer_class = TrainingTaskSerializer
    queryset = TrainingTask.objects.all()


class TrainingTaskListView(ListModelMixin, GenericTrainingTaskView):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TrainingTaskDetailView(RetrieveModelMixin, GenericTrainingTaskView):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
