# Generated by Django 2.2.6 on 2019-11-11 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0045_auto_20191111_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalrecord',
            name='content',
            field=models.TextField(blank=True, default='None'),
        ),
    ]
