# Generated by Django 2.2.6 on 2020-01-28 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0072_doctor_doc_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='doc_image',
            field=models.ImageField(blank=True, upload_to='profile_pictures'),
        ),
    ]