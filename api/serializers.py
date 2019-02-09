from rest_framework import serializers
from rest_framework.fields import SlugField

from api.models import (
    TrainingConfiguration,
    TrainingTask
)


class TrainingConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingConfiguration
        fields = (
            'id', 'algorithm', 'dockerfile', 'created_on',
        )

    algorithm = SlugField(label='name')
    dockerfile = SlugField(label='name')


class TrainingTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingTask
        fields = (
            'training_configuration',
            'id',
            'status',
            'created_on',
            'started_on',
            'terminated_on',
            'failure_message',
            'test_loss',
            'test_accuracy',
            'docker_id',
        )

    docker_id = serializers.CharField(allow_null=True)
    failure_message = serializers.CharField(allow_blank=True)
    id = serializers.IntegerField(read_only=True)
    training_configuration = serializers.PrimaryKeyRelatedField(read_only=True)
    started_on = serializers.DateTimeField(allow_null=True)
    terminated_on = serializers.DateTimeField(allow_null=True)
