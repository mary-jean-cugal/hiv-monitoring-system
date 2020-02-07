from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms
from datetime import date
from patient.models import Patient


class AdminNotification(models.Model): 
	name = models.CharField(default="None", max_length = 100, blank=True)
	user_type = models.CharField(default="None", max_length = 15, blank=True)
	notif = models.CharField(default="None", max_length = 100, blank=True)
	created_on = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.name