# Generated by Django 2.2.7 on 2020-02-12 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0077_auto_20200201_1510'),
        ('patient', '0099_auto_20200212_0335'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalrecord',
            name='docs_viewed',
            field=models.ManyToManyField(blank=True, to='doctor.UsersViewed'),
        ),
    ]
