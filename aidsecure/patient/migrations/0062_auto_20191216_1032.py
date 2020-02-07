# Generated by Django 2.2.6 on 2019-12-16 02:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0061_auto_20191216_0144'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('username', models.CharField(blank=True, default='none', max_length=200)),
                ('drug_name', models.CharField(blank=True, default='none', max_length=200)),
                ('unit_of_measure', models.CharField(blank=True, default='none', max_length=200)),
                ('intake_per_bottle', models.CharField(blank=True, default='none', max_length=200)),
                ('administered', models.BooleanField(blank=True, default=False)),
                ('administered_by', models.CharField(blank=True, default='none', max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Medication',
            },
        ),
        migrations.AlterField(
            model_name='patient',
            name='medical_history',
            field=models.ManyToManyField(blank=True, null=True, to='patient.MedHistForm'),
        ),
    ]
