# Generated by Django 2.2.6 on 2019-11-06 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cebuMap', '0010_auto_20191106_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cebumap',
            name='ceb_map',
            field=models.URLField(default='http://localhost:8000/cebuMap', max_length=250),
        ),
    ]
