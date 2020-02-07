# Generated by Django 2.2.6 on 2019-11-20 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0036_remark_remark_parent_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='remark',
            name='doc_views_details',
        ),
        migrations.RemoveField(
            model_name='remark',
            name='remark_parent_type',
        ),
        migrations.AddField(
            model_name='remark',
            name='remark_seen',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]