# Generated by Django 2.2.6 on 2019-12-20 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0053_monthlystatistics_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlystatistics',
            name='doctor_name',
            field=models.CharField(blank=True, default='None', max_length=100),
        ),
    ]
