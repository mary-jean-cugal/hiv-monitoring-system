# Generated by Django 2.2.6 on 2019-11-06 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cebuMap', '0012_auto_20191106_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cebumap',
            name='ceb_map',
            field=models.URLField(verbose_name='http://localhost:8000/cebuMap'),
        ),
    ]
