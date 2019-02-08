from django.contrib import admin

from api.models import TrainingConfiguration


@admin.register(TrainingConfiguration)
class TrainingConfigurationAdmin(admin.ModelAdmin):
    model = TrainingConfiguration
    list_display = ('id', 'created_on', 'algorithm_name', )

    def algorithm_name(self, instance):
        return instance.algorithm.name if instance.algorithm else ""
