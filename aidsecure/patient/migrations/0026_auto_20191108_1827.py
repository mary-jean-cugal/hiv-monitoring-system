# Generated by Django 2.2.6 on 2019-11-08 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0025_auto_20191108_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientlocationdetails',
            name='username',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='patientlocationdetails',
            name='work',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]