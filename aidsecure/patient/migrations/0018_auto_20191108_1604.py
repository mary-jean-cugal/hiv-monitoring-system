# Generated by Django 2.2.6 on 2019-11-08 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0017_auto_20191108_1601'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='medhist',
            new_name='medical_history',
        ),
    ]
