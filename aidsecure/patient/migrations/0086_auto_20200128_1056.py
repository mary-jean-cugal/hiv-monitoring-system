# Generated by Django 2.2.6 on 2020-01-28 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0085_auto_20200127_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medhistform',
            name='date_diagnosed',
            field=models.DateField(blank=True),
        ),
    ]