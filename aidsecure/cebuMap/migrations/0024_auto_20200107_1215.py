# Generated by Django 2.2.6 on 2020-01-07 04:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cebuMap', '0023_auto_20191213_1716'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cebubarangays',
            old_name='no_hiv',
            new_name='for_screening',
        ),
    ]
