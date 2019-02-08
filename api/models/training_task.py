from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TrainingTask(models.Model):
    CREATED = "created"
    BUILDING = "building"
    TRAINING = "training"
    COMPLETE = "complete"
    ABORTED = "aborted"
    FAILURE = "failure"

    STATUS_CHOICES = (
        (CREATED, _("Created")),
        (BUILDING, _("Building")),
        (TRAINING, _("Training")),
        (COMPLETE, _("Complete")),
        (ABORTED, _("Abordted")),
        (FAILURE, _("Failure")),
    )

    training_configuration = models.ForeignKey(
        'api.TrainingConfiguration',
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    status = models.CharField(
        help_text=_("Task status"),
        max_length=16,
        choices=STATUS_CHOICES,
        default=CREATED
    )
    created_on = models.DateTimeField(auto_now_add=True)
    started_on = models.DateTimeField(null=True, blank=True)
    terminated_on = models.DateTimeField(null=True, blank=True)
    failure_message = models.TextField(
        help_text=_("Failure logs"),
        null=True,
        blank=True
    )
    test_loss = models.DecimalField(
        help_text=_("Algorithm loss in percents."),
        null=True, blank=True,
        max_digits=9,
        decimal_places=6,
        validators=[
            MinValueValidator(Decimal("0")),
            MaxValueValidator(Decimal("100")),
        ]
    )
    test_accuracy = models.DecimalField(
        help_text=_("Algorithm loss in percents."),
        null=True, blank=True,
        max_digits=9,
        decimal_places=6,
        validators=[
            MinValueValidator(Decimal("0")),
            MaxValueValidator(Decimal("100")),
        ]
    )

    def clean_fields(self, exclude=None):
        if exclude is None:
            exclude = []

        if 'terminated_on' not in exclude:
            self.clean_terminated_on()

        if 'started_on' not in exclude:
            self.clean_started_on()

    def clean_terminated_on(self):
        if self.terminated_on is None:
            return

        if self.terminated_on < self.created_on:
            raise ValidationError({
                'terminated_on': _(
                    "End date cannot be before build creation date."
                )
            })

        if self.started_on is None:
            raise ValidationError({
                'terminated_on':_(
                    'Cannot set end-date without a start date.')
            })

        if self.terminated_on < self.started_on:
            raise ValidationError({
                'terminated_on': _(
                    'End date cannot be before script start date.')
            })

    def clean_started_on(self):
        if self.started_on is None:
            return

        if self.started_on < self.created_on:
            raise ValidationError({
                'started_on': _(
                    'Start date cannot be before script execution scheduling '
                    'date.'
                )
            })
