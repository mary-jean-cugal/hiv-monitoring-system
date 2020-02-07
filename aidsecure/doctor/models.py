from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

from datetime import datetime, date, timezone


# ARV = Antiretroviral Drugs
# ART = Antiretroviral Therapy
class Medicine(models.Model):
	created_on = models.DateTimeField(default=datetime.now, blank=True) 
	availability = models.BooleanField(default=False, blank=True)
	
	drug_group = models.CharField(default="none", max_length=200, blank=True) # ART SDF, ART FDC, ART for Pedia
	drug_name = models.CharField(default="none", max_length=200, blank=True)
	medicine_type = models.CharField(default="none", max_length=200, blank=True) #tablet, liquid
	unit_of_measure = models.CharField(default="none", max_length=200, blank=True) # ml, (1 pc)mg
	content_per_bottle = models.IntegerField(default=0, blank=True) # 30 (ml), 40 (pcs)
	
	patients_on_medication = models.IntegerField(default=0, blank=True) # count of patients taking the medicine 
	stocks_on_hand = models.IntegerField(default=0, blank=True) # count of bottles


	def __str__(self):
		return self.drug_name
		
# lets users know who viewed a file e.g. a remark
class UsersViewed(models.Model):
	seen_flag = models.BooleanField(default=False, blank=True) #?? not sure if useful
	seen_date = models.DateTimeField(default=datetime.now, blank=True)
	file_owner = models.CharField(default="None", max_length=100, blank=True) #name of the owner of the file viewed
	viewer_type = models.CharField(default="None", max_length=100, blank=True) # viewed by patient or doctor
	viewed_type = models.CharField(default="None", max_length=100, blank=True) # if type == Patient User: Comment,  Medhist Remark, ICR Remark, Prof Remark, Consultation Schedule Remark |  DoctorUser: Personal Record,  Consultation Schedule, ICR, Medical History, Profile Form
	viewer_name = models.CharField(default="None", max_length=100, blank=True) # name for doctor and username for patient
	viewed_pk = models.IntegerField(default=0, blank=True)

	def __str__(self):
		return self.viewer_name
	class Meta:
		verbose_name_plural = "Users Viewed"



# remark is used for ICR, PROFILE, MED HIST AND SCHEDULES ONLY
class Remark(models.Model):
	author = models.CharField(default="None", max_length=200, blank=True)
	text = models.TextField(default="None", blank=True)
	created_date = models.DateTimeField(default=datetime.now, blank=True)
	approved_comment = models.BooleanField(default=False) # not useful atm
	remark_parent_type = models.CharField(default="None", max_length=100, blank=True) # for navigation purposes sa admin:  Consultation Schedule, ICR, Medical History, Profile Form, Personal Record
	remark_receiver =  models.CharField(default="None", max_length=100, blank=True)  # for navigation purposes sa admin
	remark_seen = models.BooleanField(default=False,  blank=True) # patient has seen or not
	seen_date = models.DateTimeField(default=datetime.now, blank=True)

	def __str__(self):
	    return self.author

# updates the doctor's monthly stats when a patient adds a doctor 
# takes note of the number of patients added in a month over the number of patients who joined the website on that month 
class MonthlyStatistics(models.Model):
	created_on = models.DateTimeField(default=datetime.now, blank=True)
	doctor_name = models.CharField(default="None", max_length = 100, blank=True)
	doc_pk = models.IntegerField(default=0, blank=True)
	patient_pk =  models.IntegerField(default=0, blank=True) # stores the patient pk for searching the patient added
	year = models.CharField(default="2019", max_length = 10, blank=True)

	january = models.IntegerField(default=0, blank=True)
	february = models.IntegerField(default=0, blank=True)
	march = models.IntegerField(default=0, blank=True)
	april = models.IntegerField(default=0, blank=True)
	may = models.IntegerField(default=0, blank=True)
	june = models.IntegerField(default=0, blank=True)
	july = models.IntegerField(default=0, blank=True)
	august = models.IntegerField(default=0, blank=True)
	september = models.IntegerField(default=0, blank=True)
	october = models.IntegerField(default=0, blank=True)
	november = models.IntegerField(default=0, blank=True)
	december = models.IntegerField(default=0, blank=True)

	class Meta:
		verbose_name_plural = "Monthly Statistics"
		get_latest_by = 'created_on'
		ordering = ['-created_on']
		
	def __str__(self):
		return self.doctor_name
	

class DoctorStats(models.Model):
	# updated_on = models.DateTimeField(default=datetime.now, blank=True)
	day_count = models.IntegerField(default=0) # way gamit
	last_updated =  models.DateField(default=datetime.now, blank=True)
	start_date = models.DateField(default=datetime.now, blank=True)
	week_count = models.IntegerField(default=0, blank=True) # way gamit
	doctor_name = models.CharField(default="None", max_length = 100, blank=True)
	for_screening = models.IntegerField(default=0, blank=True)
	neg_patients = models.IntegerField(default=0, blank=True)  # and positive
	stage_1 = models.IntegerField(default=0, blank=True)
	stage_2 = models.IntegerField(default=0, blank=True)
	stage_3 = models.IntegerField(default=0, blank=True)
	all_patients_count = models.IntegerField(default=0, blank=True)
	doc_patients_count = models.IntegerField(default=0, blank=True)

	monthly_stats = models.ManyToManyField(MonthlyStatistics, blank=True)

	class Meta:
		verbose_name_plural = "Patients Statistics"

	def __str__(self):
		return self.doctor_name
	


class DoctorSchedule(models.Model): 
	patient_username = models.CharField(default="None", max_length = 100, blank=True)
	patient_hiv_status = models.CharField(default="None", max_length = 100, blank=True)
	schedule_date = models.DateTimeField(default=datetime.now, blank=True)
	schedule_topic = models.CharField(default="None", max_length = 200, blank=True)
	schedule_notes = models.TextField(default="None", blank=True)
	doc_in_charge = models.CharField(default="None", max_length = 100, blank=True)
	status = models.CharField(default="None", max_length = 20, blank=True) # status: pending, on going, finished, rejected
	action_taken = models.IntegerField(default=0, blank=True) # 0 = none, 1 = accepted, 2 = rejected, 3 = finished useful in getting sched in notifs
	created_on = models.DateTimeField(default=datetime.now, blank=True)

	new_notif_count = models.IntegerField(default=0) #way gamitt??

	doc_remark = models.ManyToManyField(Remark, blank=True)
	users_viewed = models.ManyToManyField(UsersViewed,  blank=True)

	class Meta:
		verbose_name_plural = "Schedules"
		ordering = ['-created_on']

	def __str__(self):
		return self.patient_username


class DoctorNotification(models.Model):  
	created_on = models.DateTimeField(default=datetime.now, blank=True)
	name = models.CharField(default="None", max_length = 100, blank=True) # name of doctor, for documentation purposes in admin
	subject = models.CharField(default="None", max_length = 100, blank=True) # ICR Form, Appointment, Patient, Doctors List, Present Address 
	user_type = models.CharField(default="None", max_length = 15, blank=True)   #patient, admin
	notif = models.CharField(default="None", max_length = 2000, blank=True)
	patient_username = models.CharField(default="None", max_length=100, blank=True)
	action_type = models.CharField(default="None", max_length = 100, blank=True) # New Patient, Schedule Request, Removed, Edit (patient edits icr form)
	action_pk = models.IntegerField(default=0, blank=True)  # parent pk of the action taken if remark or comment, pk of the action itself if consultation sched 
	action_taken = models.IntegerField(default=0, blank=True) # (0 = none, 1 = accepted, 2 = rejected, 3 = finished) useful in getting sched in notifs
	notif_status = models.BooleanField(default=False, blank=True) # false = unread, true= read

	class Meta:
		verbose_name_plural = "Notifications"
		ordering = ['-created_on']

	def __str__(self):
		return self.action_type

class Doctor(models.Model):
	slug = models.SlugField() # firstname + "." + "lastname"
	login_flag = models.BooleanField(default=False)
	last_log_in = models.DateTimeField(default=datetime.now, blank=True)
	last_log_out = models.DateTimeField(default=datetime.now, blank=True)
	
	name = models.CharField(default="none", max_length=100, blank=True) # First name Middle name with period and Lastname
	field_specialty = models.CharField(default="none", max_length=100, blank=True) # field specialty doctor studied
	position = models.CharField(default="none", max_length=100, blank=True) # position at the facility doctor works in 
	birthdate = models.DateField(default= date.today, blank=True)
	phone_number = models.CharField(default="none", max_length=20, blank=True)
	email = models.CharField(default="none", max_length=100, blank=True)
	hospital_name = models.CharField(default="none", max_length=100, blank=True)
	hospital_address = models.CharField(default="none", max_length=200, blank=True)
	password = models.CharField(default="none", max_length=100, blank=True)
	doc_image = models.ImageField(upload_to='profile-pictures', blank=True)
	
	doctorNotifs = models.ManyToManyField(DoctorNotification, blank=True)
	new_notifs = models.ManyToManyField(DoctorNotification, related_name="new_doc_notifs", blank=True)

	schedules = models.ManyToManyField(DoctorSchedule, blank=True) #accepted schedules
	pending_scheds =  models.ManyToManyField(DoctorSchedule, related_name="doc_pending_scheds", blank=True)
	rejected_scheds = models.ManyToManyField(DoctorSchedule, related_name="doc_rejected_scheds", blank=True)
	finished_scheds = models.ManyToManyField(DoctorSchedule, related_name="doc_finished_scheds", blank=True)
	p_handled_stats = models.OneToOneField(DoctorStats,  on_delete="models.CASCADE", unique=True, null=True, blank=True)


	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('doctor_detail', kwargs={'slug': self.slug})


	def removePendingSched(self, sched):
		for p_sched in self.pending_scheds.all():
			if p_sched.patient_username == sched.patient_username and p_sched.schedule_topic == sched.schedule_topic and sched.created_on == p_sched.created_on:
				self.pending_scheds.remove(p_sched)
		return list(self.pending_scheds.all())
		

