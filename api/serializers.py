from rest_framework import serializers
from rest_framework.fields import DateTimeField, SlugField

from api.models import TrainingConfiguration


class TrainingConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingConfiguration
        fields = (
            'id', 'algorithm', 'dockerfile', 'created_on',
        )

    algorithm = SlugField(label='name')
    dockerfile = SlugField(label='name')
