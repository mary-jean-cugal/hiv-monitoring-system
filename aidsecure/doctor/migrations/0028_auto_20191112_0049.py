# Generated by Django 2.2.6 on 2019-11-11 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0027_auto_20191112_0038'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='doctornotification',
            options={'ordering': ['-created_on'], 'verbose_name_plural': 'Notifications'},
        ),
        migrations.AlterModelOptions(
            name='doctorschedule',
            options={'ordering': ['-created_on'], 'verbose_name_plural': 'Schedules'},
        ),
    ]
