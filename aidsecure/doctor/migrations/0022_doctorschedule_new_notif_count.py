# Generated by Django 2.2.6 on 2019-11-10 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0021_auto_20191111_0043'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorschedule',
            name='new_notif_count',
            field=models.IntegerField(default=0),
        ),
    ]