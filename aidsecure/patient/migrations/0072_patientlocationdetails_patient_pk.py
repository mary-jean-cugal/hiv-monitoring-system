# Generated by Django 2.2.6 on 2020-01-03 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0071_patient_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientlocationdetails',
            name='patient_pk',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]