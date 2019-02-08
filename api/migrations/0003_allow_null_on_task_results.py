# Generated by Django 2.1.5 on 2019-02-08 22:13

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_trainingtask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainingtask',
            name='test_accuracy',
            field=models.DecimalField(blank=True, decimal_places=6, help_text='Algorithm loss in percents.', max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('100'))]),
        ),
        migrations.AlterField(
            model_name='trainingtask',
            name='test_loss',
            field=models.DecimalField(blank=True, decimal_places=6, help_text='Algorithm loss in percents.', max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('100'))]),
        ),
    ]