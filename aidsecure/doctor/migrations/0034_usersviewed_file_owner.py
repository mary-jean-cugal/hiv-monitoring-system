# Generated by Django 2.2.6 on 2019-11-19 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0033_auto_20191120_0116'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersviewed',
            name='file_owner',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]