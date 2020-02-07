# Generated by Django 2.2.6 on 2019-11-10 16:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0019_auto_20191111_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='last_log_in',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='last_log_out',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
