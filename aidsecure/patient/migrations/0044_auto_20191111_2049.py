# Generated by Django 2.2.6 on 2019-11-11 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0043_auto_20191111_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientnotification',
            name='notification',
            field=models.CharField(blank=True, default='None', max_length=1000),
        ),
    ]