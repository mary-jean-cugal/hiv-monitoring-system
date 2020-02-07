# Generated by Django 2.2.6 on 2020-01-17 08:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0060_auto_20200117_1628'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='doctor',
            options={'ordering': ['-created_on']},
        ),
        migrations.AlterModelOptions(
            name='doctorstats',
            options={'ordering': ['-created_on'], 'verbose_name_plural': 'Patients Statistics'},
        ),
        migrations.AddField(
            model_name='doctor',
            name='created_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='doctorstats',
            name='created_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
