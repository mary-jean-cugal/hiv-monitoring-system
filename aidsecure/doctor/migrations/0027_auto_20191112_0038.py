# Generated by Django 2.2.6 on 2019-11-11 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0046_auto_20191112_0038'),
        ('doctor', '0026_auto_20191111_2054'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Note',
            new_name='Remark',
        ),
    ]
