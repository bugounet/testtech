import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from api.models import TrainingTask


class TestTaskValidation(TestCase):
    def test_null_terminated_on_doesnt_raise_a_validation_error(self):
        task = TrainingTask(terminated_on=None)

        task.clean_terminated_on()

    def test_terminated_on_before_created_on_raise_a_validation_error(self):
        task = TrainingTask(
            created_on=datetime.datetime(2019,1,2, 0, 0, 0),
            terminated_on=datetime.datetime(2019,1,1,23,59,0)
        )

        with self.assertRaises(ValidationError):
            task.clean_terminated_on()

    def test_terminated_on_without_started_on_rasies_a_validation_error(self):
        task = TrainingTask(
            created_on=datetime.datetime(2019, 1, 2, 0, 0, 0),
            terminated_on=datetime.datetime(2019, 1, 2, 23, 59, 0),
            started_on=None,
        )

        with self.assertRaises(ValidationError):
            task.clean_terminated_on()

    def test_terminated_on_before_started_on_rasies_a_validation_error(self):
        task = TrainingTask(
            created_on=datetime.datetime(2019, 1, 2, 0, 0, 0),
            terminated_on=datetime.datetime(2019, 1, 2, 23, 59, 0),
            started_on=datetime.datetime(2019, 1, 3, 0, 1, 0),
        )

        with self.assertRaises(ValidationError):
            task.clean_terminated_on()

    def test_valid_terminated_on_date_with_started_on_set(self):
        task = TrainingTask(
            created_on=datetime.datetime(2019, 1, 2, 0, 0, 0),
            terminated_on=datetime.datetime(2019, 1, 2, 23, 59, 0),
            started_on=datetime.datetime(2019, 1, 2, 12, 0, 0),
        )

        task.clean_terminated_on()

    def test_started_on_before_created_on_raises_a_validation_error(self):
        task = TrainingTask(
            created_on=datetime.datetime(2019, 1, 3, 0, 1, 0),
            started_on=datetime.datetime(2019, 1, 2, 0, 0, 0),
        )

        with self.assertRaises(ValidationError):
            task.clean_started_on()

    def test_started_on_with_none_value_doesnt_raise_a_validation_error(self):
        task = TrainingTask(
            created_on=datetime.datetime(2019, 1, 2, 0, 0, 0),
            started_on=None
        )

        task.clean_started_on()

    def test_started_on_with_value_after_created_on_doesnt_raise_an_error(self):
        task = TrainingTask(
            created_on=datetime.datetime(2019, 1, 2, 0, 0, 0),
            started_on=datetime.datetime(2019, 1, 3, 0, 1, 0),
        )

        task.clean_started_on()
