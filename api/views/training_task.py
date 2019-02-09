from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response

from api.actions import TrainingTaskActionManager
from api.exceptions import AbortNotPossible, AbortFailed
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


class TrainingTaskAbortView(GenericTrainingTaskView):
    def post(self, request, *args, **kwargs):
        training_task = self.get_object()
        actions = TrainingTaskActionManager(training_task)
        try:
            actions.abort()
        except AbortNotPossible as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except AbortFailed as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response("", status=status.HTTP_202_ACCEPTED)
