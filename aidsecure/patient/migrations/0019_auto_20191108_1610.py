# Generated by Django 2.2.6 on 2019-11-08 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0018_auto_20191108_1604'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='locationDetails',
            new_name='location_details',
        ),
    ]
