import os
from uuid import uuid4

from django.db import models
from django.utils.translation import ugettext_lazy as _


def get_algorithm_path(instance, filename):
    last_id = (
        instance.id or
        TrainingConfiguration.objects.count()+1
    )
    return os.path.join(
        "docker-images", "algorithm_{}".format(last_id), filename
    )


class TrainingConfiguration(models.Model):
    """ Training model configuration: bindls together dockerfile, python
    algorithm. It contains a creation date.
    """
    algorithm = models.FileField(
        help_text=_("Submitted python algorithm"),
        upload_to=get_algorithm_path,
    )

    dockerfile = models.FileField(
        help_text=_("Submitted dockerfile"),
        upload_to=get_algorithm_path,
    )

    created_on = models.DateTimeField(auto_now_add=True)
