# Generated by Django 2.2.6 on 2020-01-07 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0058_auto_20200107_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorstats',
            name='for_screening',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='doctorstats',
            name='neg_patients',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
