# Generated by Django 2.2.6 on 2019-12-03 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0055_auto_20191203_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='home_address',
            field=models.CharField(blank=True, default='none', max_length=100),
        ),
    ]