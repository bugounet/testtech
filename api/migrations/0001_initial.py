# Generated by Django 2.1.5 on 2019-02-08 17:21

import api.models.training_configuration
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('algorithm', models.FileField(help_text='Submitted python algorithm', upload_to=api.models.training_configuration.get_algorithm_path)),
                ('dockerfile', models.FileField(help_text='Submitted dockerfile', upload_to=api.models.training_configuration.get_algorithm_path)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
