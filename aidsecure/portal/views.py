from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib import messages
from django.http import HttpResponse

from doctor.models import Doctor, DoctorNotification, DoctorStats, Medicine, MonthlyStatistics
from patient.models import Patient, ICRForm, ProfileForm, MedHistForm, PersonalRecord, PatientLocationDetails, PatientsMonthlyStatistics
from cebuMap.models import CebuBarangays 


from datetime import datetime, date
from django.contrib.gis.geos import Point

from django.views.decorators.cache import cache_control



def setPortal(request):
	
	doctors = Doctor.objects.all()
	patients = Patient.objects.all()
	context ={
		'doctors' : doctors,
		'patients' : patients, 
	}
	return render(request, 'portal/mainPage.html', context) 


@csrf_protect 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def validateDoctor(request, slug):
	if slug:
		d = Doctor.objects.get(slug=slug)
		print(d, "-"*30)
	patient_arr = []
	pending_patients = []
	approved_patients = []
	p_none = 0
	p_stage1 = 0
	p_stage2 = 0
	p_stage3 = 0

	if 'doc-name' in request.POST:
		doc_name = (request.POST.get("doc-name")).title()
		doc_password = request.POST.get("doc-password")
		doctors = Doctor.objects.all()
		doc_exists = doctors.filter(name=doc_name, password=doc_password).exists()
		if doc_exists:
			print("doc exists: " + doc_name + " "+"*"*30)
			doctor = Doctor.objects.get(name=doc_name)
			patients = Patient.objects.all()

			# save the time doctor is logged in 
			if doctor.login_flag is False: # prevent resetting last log in on  page refresh
				doctor.last_log_in = datetime.now() 
				doctor.login_flag=True

			# load new notifications since log out
			for notif in doctor.doctorNotifs.all():
				if notif.created_on >= doctor.last_log_out:
					doctor.new_notifs.add(notif)

			# load data for doctor statistics
			for_screening_count = 0
			neg_count = 0
			stage1_count = 0
			stage2_count = 0
			stage3_count = 0
			
			for p in patients:
				if p.my_doctors.filter(name=doc_name).exists():
					if (p.HIV_status == "for screening"):
						for_screening_count+=1
					if (p.HIV_status == "negative"):
						neg_count+=1
					elif (p.HIV_status == "stage 1"):
						stage1_count+=1
					elif (p.HIV_status == "stage 2"):
						stage2_count+=1
					elif (p.HIV_status == "stage 3"):
						stage3_count+=1
					patient_arr.append(p)			
					
			doctor.p_handled_stats.for_screening = for_screening_count		
			doctor.p_handled_stats.neg_patients = neg_count
			doctor.p_handled_stats.stage_1 = stage1_count
			doctor.p_handled_stats.stage_2 = stage2_count
			doctor.p_handled_stats.stage_3 = stage3_count
			doctor.p_handled_stats.all_patients_count = Patient.objects.all().count()
			doctor.p_handled_stats.doc_patients_count = len(patient_arr)
			doctor.p_handled_stats.save()

			doctor.save() # to save all the changes made to doctor object


			meds = Medicine.objects.all()
			all_patients = Patient.objects.all()
			all_patients_stat = PatientsMonthlyStatistics.objects.all()

			context={
				'doctor' : doctor,
				'patients': patient_arr,
				'all_patients': all_patients,
				'patients_stats': all_patients_stat,
				'medicines': meds
			}
			request.session['doc-name-local'] = doctor.name
			return render(request, 'doctor/doctor.html',  context)
	return render(request, 'portal/mainPage.html')


@csrf_protect
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def validatePatient(request, slug): 	
	if 'patient-username' in request.POST:
		patient_username = request.POST.get("patient-username")
		patient_password = request.POST.get("patient-password")
		patients = Patient.objects.all()
		patient_exists = patients.filter(username=patient_username, password=patient_password).exists()
		if patient_exists:
			doctors = Doctor.objects.all()
			patient = Patient.objects.get(username=patient_username)

			# save latest log in date and time
			if patient.login_flag is False: # prevent resetting last log in on  page refresh
				patient.last_log_in = datetime.now() 
				patient.login_flag = True

			
			# load new notifications since log out
			patient.patient_new_notifications.clear()
			for notif in patient.patient_notifications.all():
				if notif.status == True:
					patient.patient_new_notifications.add(notif)
			patient.save()

			context={
				'patient' :  patient,
				'doctors': doctors,
			}
			request.session['patient-uname-local'] = patient.username
			return render(request,'patient/patient.html', context)
	return render(request, 'portal/mainPage.html')



# @csrf_exempt
def addPatient(request): 
	if 'p-first-name' in request.POST:
		doctors = Doctor.objects.all()
		patient_dir = Patient.objects.all()
		
		icr = ICRForm()
		new_patient = Patient()

		icr.save()
		
		loc_details = PatientLocationDetails.objects.create()
		loc_details.created_on = datetime.now()

		lat = request.POST.get('lat', "")
		lon = request.POST.get('lon', "")

		home_add = request.POST.get('p-home-address', "")
		present_add = request.POST.get('p_present_address', "")
		first_name = request.POST.get('p-first-name', "")
		last_name = request.POST.get('p-last-name', "")
		username = request.POST.get('p-username', "") 
		occupation = request.POST.get('p-occupation', "")
		status = request.POST.get('p-status', "")
		age = request.POST.get('p-age', "")
		bdate = request.POST.get('p-birthdate', "")
		phone_num = request.POST.get('p-phone-number', "")
		tel_num = request.POST.get('tel-number', "")
		work_add = request.POST.get('p-work-address', "")
		email = request.POST.get('p-email', "")
		password = request.POST.get('p_password', "")

		has_f_name = False
		has_l_name = False
		# make sure that no null value is passed
	
		if len(home_add) > 0:
			new_patient.home_address = home_add.title()
		if len(present_add) > 0:
			new_patient.present_address = present_add.title()
		if len(first_name) > 0:
			has_f_name = True
			new_patient.first_name  = first_name.title()
		if len(last_name) > 0:
			has_l_name=True
			new_patient.last_name= last_name.title()
		if len(username) > 0:
			new_patient.username = username
			new_patient.slug = "patient-" + username
		if len(occupation) > 0:
			new_patient.work = occupation.lower().title()
		if len(status) > 0:
			new_patient.HIV_status = status.lower() 
		if len(age):
			new_patient.age = age
		if len(bdate) > 0: 
			new_patient.birthdate = bdate.lower()
		if len(phone_num) > 0:
			new_patient.call_number = phone_num
		if len(tel_num) > 0:
			new_patient.tel_number = tel_num
		if len(work_add) > 0:
			new_patient.work_address = work_add.lower().title()
		if len(email) > 0:
			new_patient.email = email
		if len(password) > 0:
			new_patient.password = password

		patient_exists = patient_dir.filter(first_name=new_patient.first_name, last_name=new_patient.last_name, username=new_patient.username).exists()
		if patient_exists:
			new_patient = None
			return render(request,'portal/mainPage.html')
		else:
			# create icr form for patient
			icr.first_name = new_patient.first_name
			icr.last_name = new_patient.last_name
			icr.birthdate = new_patient.birthdate
			icr.age = new_patient.age
			icr.phone_number = new_patient.call_number
			icr.home_address = new_patient.home_address 
			icr.occupation = new_patient.work
			icr.work_address = new_patient.work_address
			icr.save()
			new_patient.icr = icr
			new_patient.icr.save()


			# create medhist form for patient	 
			medhist = MedHistForm() 						#keep date diagnosed and other medical conditions null when adding a new patient
			medhist.name = new_patient.first_name + " " + new_patient.last_name
			medhist.username = new_patient.username
			if new_patient.HIV_status == "for screening":
				medhist.exposure = "for screening"
			elif new_patient.HIV_status == "negative":
				medhist.exposure = "negative"
			else:
				medhist.exposure = "positive"

			#  create Location Details for the patient
			if len(lat) > 0:
				loc_details.lat = lat
			if len(lon) > 0:
				loc_details.lon = lon

			if PatientLocationDetails.objects.all().filter(lat=loc_details.lat, lon=loc_details.lon).exists():
				print("duplicate location", '*'*50)
				while PatientLocationDetails.objects.all().filter(lat=loc_details.lat, lon=loc_details.lon).exists():
					loc_details.lon = str(float(loc_details.lon) + 0.001) #add .001 to create only unique locations
					loc_details.lat = str(float(loc_details.lat) + 0.001) #add .001 to create only unique locations
			loc_details.patient_pk = new_patient.pk
			loc_details.username = new_patient.username
			loc_details.work = new_patient.work
			loc_details.location = new_patient.present_address
			loc_details.patient_name = new_patient.first_name + " " + new_patient.last_name
			loc_details.hiv_level = new_patient.HIV_status
			if "cebu" in (new_patient.present_address).lower(): 
				loc_details.general_location = "within cebu"
			else:
				loc_details.general_location = "outside cebu"
			
			# create a new Monthly Statistics to update all patients count
			if PatientsMonthlyStatistics.objects.all().count() > 0:
				patients_monthly_stat = PatientsMonthlyStatistics.objects.latest()
				patients_monthly_stat.pk = patients_monthly_stat.pk + 1 
			else:		
				patients_monthly_stat =  PatientsMonthlyStatistics()
			patients_monthly_stat.created_on = datetime.now()
			patients_monthly_stat.patient_pk = new_patient.pk
			patients_monthly_stat.year = datetime.now().year
			patients_monthly_stat.patient_username = new_patient.username
			
			if new_patient.date_created.month == 1:
				patients_monthly_stat.january+=1
			elif new_patient.date_created.month == 2:
				patients_monthly_stat.february+=1
			elif new_patient.date_created.month == 3:
				patients_monthly_stat.march+=1
			elif new_patient.date_created.month == 4:
				patients_monthly_stat.april+=1
			elif new_patient.date_created.month == 5:
				patients_monthly_stat.may+=1
			elif new_patient.date_created.month == 6:
				patients_monthly_stat.june+=1
			elif new_patient.date_created.month == 7:
				patients_monthly_stat.july+=1
			elif new_patient.date_created.month == 8:
				patients_monthly_stat.august+=1
			elif new_patient.date_created.month == 9:
				patients_monthly_stat.september+=1
			elif new_patient.date_created.month == 10:
				patients_monthly_stat.october+=1
			elif new_patient.date_created.month == 11:
				patients_monthly_stat.november+=1
			elif new_patient.date_created.month == 12:
				patients_monthly_stat.december+=1
			patients_monthly_stat.save()

			# save all the objects with a relationship to patient that have been added with data
			loc_details.save()
			new_patient.date_created = datetime.now()
			new_patient.save()
			medhist.parent_pk = new_patient.pk
			medhist.save()
			new_patient.medical_history.add(medhist)
			new_patient.save()  #save first so that a pk can be generated and a foreign key can be added
			new_patient.location_details.add(loc_details)
			new_patient.save()


			# add patient to barangay he/she belongs for data summary at map
			patient_point = Point(float(new_patient.location_details.latest().lon), float(new_patient.location_details.latest().lat))
			if CebuBarangays.objects.filter(geom__intersects=patient_point).exists():
				brgy = CebuBarangays.objects.get(geom__intersects=patient_point)

				# don't add to hiv population if for screening or negative. they're not part of the HIV population
				if new_patient.HIV_status == "for screening":
					brgy.for_screening.add(new_patient)
				elif  new_patient.HIV_status == "negative":
					brgy.stage_0.add(new_patient)
				else:
					brgy.hiv_pop.add(new_patient)
					if  new_patient.HIV_status == "stage 1":
						brgy.stage_1.add(new_patient)
					elif  new_patient.HIV_status == "stage 2":
						brgy.stage_2.add(new_patient)
					elif  new_patient.HIV_status == "stage 3":
						brgy.stage_3.add(new_patient)
				
				brgy.save()
			
		doctors = Doctor.objects.all()
		patients = Patient.objects.all()
		context ={
			'doctors' : doctors,
			'patients' : patients, 
		}
		return render(request, 'portal/mainPage.html', context)
	return render(request, 'portal/mainPage.html')
			

def addDoctor(request):
	# .title() capitalize letter every after space
	doctors = Doctor.objects.all()
	new_doctor = Doctor()
	if 'doc-first-name' in request.POST:
		doc_fname = request.POST.get('doc-first-name', "") 
		doc_mname = request.POST.get('doc-middle-name', "")
		doc_lname = request.POST.get('doc-last-name', "")
		doc_bdate = request.POST.get('doc-bdate', "") # way gamit
		doc_email = request.POST.get('doc-email', "")	
		doc_phone_num = request.POST.get('doc-phone-number', "")	
		doc_position = request.POST.get('doc-position', "")
		doc_specialty = request.POST.get('doc-specialty', "")
		doc_hospital_address = request.POST.get('doc-hospital-address', "")
		doc_hospital_name = request.POST.get('doc-hospital-name', "")
		doc_hospital_name_others = request.POST.get('doc-hospital-name-others', "")
		doc_password = request.POST.get('doc_password', "")
#		new_doctor.save()
		if len(doc_fname) > 0 and len(doc_mname) > 0 and len(doc_lname) > 0:
			new_doctor.name = doc_fname.title() + " " + doc_mname.title() + " " + doc_lname.title() 
			new_doctor.slug = doc_fname.lower() + "-" + doc_mname +"-" + doc_lname.lower() 
		if len(doc_bdate) > 0:
			print(doc_bdate + "-"*50)
			new_doctor.birthdate = doc_bdate.lower()
		if len(doc_email) > 0:
			new_doctor.email = doc_email
		if doc_phone_num is not None or len(doc_phone_num) > 0:
			new_doctor.phone_number = doc_phone_num
		if len(doc_position) > 0:
			new_doctor.position = doc_position.title()
		if len(doc_specialty) > 0:
			new_doctor.field_specialty = doc_specialty.title()
		if len(doc_hospital_name):
			new_doctor.hospital_name = doc_hospital_name.title()
		else:
			new_doctor.hospital_name = doc_hospital_name_others.title()
		if len(doc_hospital_address) > 0:
			new_doctor.hospital_address = doc_hospital_address.title()
		if len(doc_password) > 0:
			new_doctor.password = doc_password
		print("DOCTOR SAVED!!!---------------------")
		new_doctor.save()
		# creates a blank stats and monthly stats
		doc_stats = DoctorStats()
		doc_stats.doctor_name = new_doctor.name
		doc_stats.neg_patients = 0
		doc_stats.stage_1 = 0
  
		monthly_stat = MonthlyStatistics.objects.create()
		monthly_stat.created_on = datetime.now()
		monthly_stat.doctor_name = new_doctor.name
		monthly_stat.pk = new_doctor.pk
		monthly_stat.year = datetime.now().year
		monthly_stat.doctor_name = new_doctor.name
		monthly_stat.save()
		
		doc_stats.save()
		doc_stats.monthly_stats.add(monthly_stat)
		
		new_doctor.p_handled_stats = doc_stats		
		
		new_doctor.save()
		
		doctors = Doctor.objects.all()
		patients = Patient.objects.all()
		context ={
			'doctors' : doctors,
			'patients' : patients, 
		}
		print("SAVING DONE!--------------------------------------")
		return render(request, 'portal/mainPage.html', context)
		
	return render(request, 'portal/mainPage.html')






