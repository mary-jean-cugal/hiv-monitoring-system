# Generated by Django 2.2.6 on 2020-01-23 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0076_auto_20200109_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientlocationdetails',
            name='gen_loc',
            field=models.CharField(blank=True, default='none', max_length=100),
        ),
    ]