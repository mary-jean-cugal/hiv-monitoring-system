# Generated by Django 2.2.6 on 2019-11-20 08:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0038_auto_20191120_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='remark',
            name='seen_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]