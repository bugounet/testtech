from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django_object_actions import DjangoObjectActions

from api.actions import TrainingConfigurationActionManager
from api.models import TrainingConfiguration
from api.models import TrainingTask


class TrainingTaskInlineModelAdmin(admin.TabularInline):
    model = TrainingTask
    extra = 1


@admin.register(TrainingConfiguration)
class TrainingConfigurationAdmin(DjangoObjectActions, admin.ModelAdmin):
    model = TrainingConfiguration
    list_display = ('id', 'created_on', 'algorithm_name', )
    inlines = [
        TrainingTaskInlineModelAdmin,
    ]
    change_actions = ['run_training']

    def algorithm_name(self, instance):
        return instance.algorithm.name if instance.algorithm else ""

    def run_training(self, request, instance):
        actions = TrainingConfigurationActionManager(instance)
        actions.run_training()
    run_training.short_description = _("Run training")

@admin.register(TrainingTask)
class TrainingTaskAdmin(admin.ModelAdmin):
    model = TrainingTask

    list_display = ('id', 'status', 'created_on', 'test_loss', 'test_accuracy')
