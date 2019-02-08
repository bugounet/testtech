from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('trainings', views.TrainingConfigurationListView.as_view()),
    path('training/<int:pk>', views.TrainingConfigurationDetailView.as_view()),
    path('training/<int:pk>/run', views.TrainingConfigurationRunActionView.as_view()),
    path('tasks', views.TrainingTaskListView.as_view()),
    path('task/<int:pk>', views.TrainingTaskDetailView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)