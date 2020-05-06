from django.db import models

class Backup(models.Model):
    name=models.CharField(max_length=100, default="Back Up Data", null=True)
    class Meta:
        verbose_name_plural = "Backup Data"

class Restore(models.Model):
    name=models.CharField(max_length=100, default="Restore Data", null=True)
    class Meta:
        verbose_name_plural = "Restore Data"



