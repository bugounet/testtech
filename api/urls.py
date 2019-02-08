from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('trainings', views.TrainingConfigurationListView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)