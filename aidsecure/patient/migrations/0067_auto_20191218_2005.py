# Generated by Django 2.2.6 on 2019-12-18 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0066_auto_20191218_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='medication',
            name='frequency',
            field=models.CharField(blank=True, default='none', max_length=200),
        ),
        migrations.AddField(
            model_name='medication',
            name='time_interval',
            field=models.CharField(blank=True, default='none', max_length=200),
        ),
    ]
