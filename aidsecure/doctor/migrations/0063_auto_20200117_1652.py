# Generated by Django 2.2.6 on 2020-01-17 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0062_auto_20200117_1647'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='monthlystatistics',
            options={'get_latest_by': 'created_on', 'verbose_name_plural': 'Monthly Statistics'},
        ),
    ]
