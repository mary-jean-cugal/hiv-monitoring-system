# Generated by Django 2.2.6 on 2019-12-18 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0064_medication_parent_pk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='medical_history',
            field=models.ManyToManyField(blank=True, to='patient.MedHistForm'),
        ),
    ]
