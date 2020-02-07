# Generated by Django 2.2.6 on 2019-11-11 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0046_auto_20191112_0038'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='icrform',
            options={'verbose_name_plural': 'Individual Client Record Forms'},
        ),
        migrations.AlterModelOptions(
            name='patientlocationdetails',
            options={'verbose_name_plural': 'Current Address Information'},
        ),
        migrations.AlterModelOptions(
            name='patientnotification',
            options={'ordering': ['-created_on'], 'verbose_name_plural': 'Notifications'},
        ),
        migrations.RemoveField(
            model_name='patient',
            name='pending_doctors',
        ),
    ]
