# Generated by Django 2.2.6 on 2019-11-26 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0051_auto_20191120_0123'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientlocationdetails',
            name='hiv_level',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
