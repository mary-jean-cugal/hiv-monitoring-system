#import os
#os.environ['DJANGO_SETTINGS_MODULE'] = 'aidsecure.settings'
from django.db import models
from django.contrib.auth.models import User

from doctor.models import Doctor, DoctorNotification, DoctorSchedule, Remark, UsersViewed
from django.utils.text import slugify
from django.urls import reverse

from datetime import datetime, date

# keeps count of the number of patients whenever added
class PatientsMonthlyStatistics(models.Model):
	created_on = models.DateTimeField(default=datetime.now, blank=True)
	patient_username = models.CharField(default="none", max_length=100, blank=True) #username of the newly added patient
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
		verbose_name_plural = "Patients Monthly Statistics"
		get_latest_by = 'created_on'
		ordering = ['-created_on']
		
	def __str__(self):
		return self.year

class Medication(models.Model):
	created_on = models.DateTimeField(default=datetime.now, blank=True) 

	patient_pk = models.CharField(default="none", max_length=200, blank=True)
	username = models.CharField(default="none", max_length=200, blank=True)
	
	drug_group = models.CharField(default="none", max_length=200, blank=True) # ART SDF, ART FDC, ART for Pedia
	drug_name = models.CharField(default="none", max_length=200, blank=True)
	medicine_type = models.CharField(default="none", max_length=200, blank=True) #tablet, liquid
	unit_of_measure = models.CharField(default="none", max_length=200, blank=True) # ml, (1 pc)mg
	content_per_bottle = models.IntegerField(default=0, blank=True)
		
	administered = models.BooleanField(default=False, blank=True) #way gamit
	administered_by = models.CharField(default="none", max_length=200, blank=True) # doctor name
	doc_notes = models.TextField(default="none", blank=True) # other stuffs doctor wants to remind the patient 

	class Meta:
		verbose_name_plural = "Medication"
	def __str__(self):
		return self.username


# only creates a new instance per patient whenever the present address and coords is changed, 
# otherwise, only edits the patient's last location detail
class PatientLocationDetails(models.Model):
	
	patient_pk = models.IntegerField(default=0, blank=True)
	lat = models.CharField(default="10.3157", max_length=200, blank=True)
	lon = models.CharField(default="123.8854", max_length=200, blank=True)
	location = models.CharField(default="none", max_length=200, blank=True)
	work = models.CharField(default="none", max_length=200, blank=True)
	patient_name = models.CharField(default="none", max_length=200, blank=True)
	username = models.CharField(default="none", max_length=200, blank=True)
	hiv_level = models.CharField(default="none", max_length=200, blank=True)
	status = models.CharField(default="none", max_length=200, blank=True) # none, ongoing therapy, deceased
	general_location = models.CharField(default="none", max_length=100, blank=True) # none, within cebu,  outside cebu, set upon patient creation, only editable by admin

	created_on = models.DateTimeField(default=datetime.now, blank=True)

	class Meta:
		ordering = ['-created_on']
		get_latest_by = 'created_on'
		verbose_name_plural = "Present Address Informations"
	def __str__(self):
		return self.patient_name


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)
 
class PersonalRecord(models.Model):
	author = models.CharField(max_length=200, blank=True)
	title = models.CharField(max_length=200, blank=True)
	slug = models.SlugField(max_length=200, blank=True)
	updated_on = models.DateTimeField(default=datetime.now, blank=True)
	content = models.TextField(default="None", blank=True)
	created_on = models.DateTimeField(default=datetime.now, blank=True)
	status = models.IntegerField(choices=STATUS, default=0)
	comment = models.ManyToManyField(Remark, blank=True)

	docs_viewed = models.ManyToManyField(UsersViewed,  blank=True)

	
	class Meta:
		ordering = ['-created_on']
		verbose_name_plural = "Personal Records"

	def __str__(self):
		return self.title


class PatientNotification(models.Model):  #should add sender and receiver
	patient_username = models.CharField(default="None", max_length = 100, blank=True) #name of patient as receiver
	doctor_name = models.CharField(default="None", max_length = 100, blank=True) # name of doctor as sender
	subject = models.CharField(default="None", max_length = 100, blank=True) # Present Address, ART Medication, Profile Form, ICR, Medical History, Consultation Schedule, Personal Record
	user_type = models.CharField(default="None", max_length = 15, blank=True) # Doctor or Admin
	action_type = models.CharField(default="None", max_length = 15, blank=True) # Add (New Medication), Chnage(Location, Status (deceased, ongoing therapy)), Remark, Edit, Done,Accepted, Declined, Comment, new doctor
	notification = models.CharField(default="None", max_length = 2000, blank=True) 
	action_pk = models.IntegerField(default=0, blank=True) # pk of the file or form a notification is triggered e.g. pk of a personal journal, or consultation schedule
	status = models.BooleanField(default=False, blank=True) # False if old, True if new
	notif_status = models.BooleanField(default=False, blank=True) # false = unread, true= read

	created_on = models.DateTimeField(default=datetime.now, blank=True) 

	class Meta:
		ordering = ['-created_on']
		
		verbose_name_plural = "Notifications"

	def __str__(self):
		return self.subject


class MedHistForm(models.Model):
	created_on = models.DateTimeField(default=datetime.now, blank=True) 
	parent_pk = models.IntegerField(default=0, blank=True)
	username = models.CharField(default="None", max_length = 100, blank=True)
	name = models.CharField(default="None", max_length = 100, blank=True)
	exposure = models.CharField(default = 'negative', max_length = 100, blank=True)  # negative or positive
	other_conditions = models.CharField(default = 'none', max_length = 100, blank=True)
	date_diagnosed = models.DateField(null=True, blank=True)   #saved as datefield
	doctor_remarks = models.ManyToManyField(Remark, blank=True)

	docs_viewed = models.ManyToManyField(UsersViewed,  blank=True)

	class Meta:
		get_latest_by = 'created_on'
		verbose_name_plural = "Medical History Forms"

	def __str__(self):
		return self.username;


class ICRForm(models.Model):

	last_name = models.CharField(default='None', max_length = 100, blank=True)
	first_name = models.CharField(default = 'secret', max_length = 100, blank=True)
	middle_name = models.CharField(default='None', max_length = 100, blank=True)
	date_of_visit = models.CharField(default="None", max_length = 100, blank=True)
	age = models.CharField(default="0", max_length=100 ,blank=True)
	birthdate = models.CharField(default="None", max_length = 100, blank=True)
	sex = models.CharField(default='None', max_length = 100, blank=True)
	civil_status = models.CharField(default='None', max_length = 100, blank=True)
	phone_number = models.CharField(default = "0", max_length=100, blank=True) # cellphone number
	home_address = models.CharField(default='Cebu City', max_length = 100, blank=True)
	occupation = models.CharField(default='None', max_length = 100, blank=True)
	work_address = models.CharField(default='None', max_length = 100, blank=True)
	work_number = models.CharField(default="123456789", max_length=100, blank=True)
	purpose_of_visit = models.CharField(default='None', max_length=100,  blank=True)
	symptoms = models.CharField(default='None', max_length=100,  blank=True)
	specification = models.CharField(default='None', max_length=100, blank=True)
	doctor_remarks =  models.ManyToManyField(Remark, blank=True)

	docs_viewed = models.ManyToManyField(UsersViewed,  blank=True)

	class Meta:
		verbose_name_plural = "Individual Client Record Forms"
	def __str__(self):
		return self.first_name;


class ProfileForm(models.Model):
	uid = models.CharField(default="None", max_length = 100, blank=True)
	code_name = models.CharField(default="None", max_length = 100, blank=True)
	real_name = models.CharField(default="None", max_length = 100, blank=True)
	mother_maiden_name = models.CharField(default="None", max_length = 100, blank=True)
	address = models.CharField( default="None", max_length = 100, blank=True)
	province = models.CharField(default="None", max_length = 100, blank=True)
	age = models.CharField(default="0", max_length = 3, blank=True)
	sex = models.CharField(default="None", max_length = 100, blank=True)
	status = models.CharField(default="None",  max_length = 100, blank=True)
	birthdate = models.CharField(default="None", max_length = 100, blank=True)
	pdate = models.CharField(default="None", max_length = 100, blank=True)
	nation = models.CharField(default="Filipino", max_length = 100, blank=True)
	ed = models.CharField(default="None", max_length = 100, blank=True)
	occupation = models.CharField(default="None",  max_length = 100, blank=True)
	contact = models.CharField(default="None", max_length = 100, blank=True) #cellphone number 11 digits
	philNum = models.CharField(default="None", max_length = 100, blank=True) # telephone 7 digits
	doctor_remarks = models.ManyToManyField(Remark, blank=True)

	docs_viewed = models.ManyToManyField(UsersViewed,  blank=True)

	class Meta:
		verbose_name_plural = "Profile Forms"
	def __str__(self):
	    return self.real_name;	

class Patient(models.Model):
	slug = models.SlugField() #  patient-username for url
	status = models.CharField(default = 'none', max_length = 100, blank=True) # (initial tag: none), ongoing therapy, deceased
	date_created = models.DateTimeField(default=datetime.now, blank=True)
	
	login_flag = models.BooleanField(default=False)
	last_log_in = models.DateTimeField(default=datetime.now, blank=True)
	last_log_out = models.DateTimeField(default=datetime.now, blank=True)

	patient_image = models.ImageField(upload_to='profile-pictures', blank=True)
	first_name = models.CharField(default = 'none', max_length = 100, blank=True)
	last_name = models.CharField(default = 'none', max_length = 100, blank=True)
	username = models.CharField(default = 'none', max_length = 100, blank=True)
	birthdate = models.DateField(default= date.today, blank=True)
	age = models.IntegerField(default = 5, blank=True)
	home_address = models.CharField(default ='none', max_length = 100, blank=True)
	present_address = models.CharField(default ='none', max_length = 100, blank=True)
	work = models.CharField(default='none', max_length = 100, blank=True) #occupation
	work_address = models.CharField(default='none', max_length = 100, blank=True)
	call_number = models.CharField(default='0', max_length = 100, blank=True) #cp number
	tel_number = models.CharField(default='0', max_length = 100, blank=True)
	email = models.CharField(default='none', max_length = 100, blank=True)
	password = models.CharField(default='none', max_length = 100, null=True)
	HIV_status =  models.CharField(default='negative', max_length = 100, blank=True) #for screening, negative, stage 1, stage 2, stage 3  //(AIDS)

	medical_history = models.ManyToManyField(MedHistForm, blank=True)
	icr = models.OneToOneField(ICRForm, on_delete="models.CASCADE", primary_key=True, unique=True, blank=True)
	profile = models.OneToOneField(ProfileForm, on_delete="models.CASCADE", unique=True, null=True, blank=True)
	personal_records = models.ManyToManyField(PersonalRecord, blank=True)
	location_details = models.ManyToManyField(PatientLocationDetails, blank=True)
	
	meds = models.ManyToManyField(Medication, blank=True)
	my_doctors = models.ManyToManyField(Doctor, blank=True) #unique=true has no effect since foreignkey is used

	patient_notifications = models.ManyToManyField(PatientNotification, blank=True)
	patient_new_notifications = models.ManyToManyField(PatientNotification, related_name="new_patient_notifications", blank=True)
	
	pending_schedules = models.ManyToManyField(DoctorSchedule, related_name="patient_pending_sched", blank=True)
	approved_schedules = models.ManyToManyField(DoctorSchedule, related_name="patient_approved_sched", blank=True)
	rejected_schedules = models.ManyToManyField(DoctorSchedule, related_name="patient_rejected_scheds", blank=True)
	finished_schedules = models.ManyToManyField(DoctorSchedule, related_name="patient_finished_scheds", blank=True)

	

	

	
	def __str__(self):
		return self.username;

	def getDocList(self):
		return list(self.my_doctors.all());

	def removeDoc(self, doc):
		for doctor in self.my_doctors.all():
			if doctor.name == doc:
				self.my_doctors.remove(doctor)
		return list(self.my_doctors.all());

	def removePendingSched(self, sched):
		for p_sched in self.pending_schedules.all():
			if p_sched.patient_username == sched.patient_username and p_sched.schedule_date == sched.schedule_date:
				self.pending_schedules.remove(p_sched)
		return list(self.pending_schedules.all())

	def addAprrovedSched(self, sched):
		sched.status = "accepted"
		sched.save()
		self.approved_schedules.add(sched)
		return list(self.approved_schedules.all())









