# Generated by Django 2.2.6 on 2020-02-01 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0075_auto_20200201_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='doc_image',
            field=models.ImageField(blank=True, upload_to='profile_pictures'),
        ),
    ]
