# Generated by Django 2.2.6 on 2020-01-28 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0071_auto_20200127_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='doc_image',
            field=models.ImageField(blank=True, upload_to='profile_page'),
        ),
    ]