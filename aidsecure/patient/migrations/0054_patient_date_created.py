# Generated by Django 2.2.6 on 2019-11-29 05:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0053_auto_20191129_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='date_created',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]