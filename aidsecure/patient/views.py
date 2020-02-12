from django.shortcuts import render
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from patient.models import ProfileForm, Patient, ICRForm,  PersonalRecord, PatientNotification, PatientLocationDetails
from doctor.models import Doctor, DoctorNotification, DoctorSchedule, DoctorStats, UsersViewed, MonthlyStatistics

from datetime import datetime, date
from django.core.files.storage import FileSystemStorage
#from django.contrib.auth import logout 
#from django.views.decorators.cache import cache_control



#@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def patientLogout(request):
#	logout(request)
	try:
		patient_username = request.session['patient-uname-local']
		patient = Patient.objects.all().get(username=patient_username)
		for notif in patient.patient_notifications.all():  #mark all notifs as old
			if notif.status == True:
				notif.status = False
				notif.save()
		patient.patient_new_notifications.clear()    # prevent resetting last log put on  page refresh

		if patient.login_flag is True:
			patient.last_log_out = datetime.now()
			patient.login_flag = False
		patient.save()
	except:
		print("no more data in the session storage")
	doctors = Doctor.objects.all()
	patients = Patient.objects.all()
	context ={
		'doctors' : doctors,
		'patients' : patients, 
	}
	return render(request, 'portal/mainPage.html', context) 

def changeProfPic(request):
	if request.method == 'POST':
		if request.is_ajax():
			patient_uname = request.session['patient-uname-local']
			patient = Patient.objects.all().get(username = patient_uname)
			image = request.FILES.get('image')
			patient.patient_image.delete(save=True) # save=True to still save the model instance without the prev url
			patient.patient_image = image
			patient.save()
			return HttpResponse("upload patient profile picture success!")
	return HttpResponse("upload patient profile picture not success.")

def notifRead(request):
	notif_pk = request.POST.get("notif_pk","")
	if PatientNotification.objects.all().filter(pk=notif_pk).exists():
		read_notif = PatientNotification.objects.all().get(pk=notif_pk)

		read_notif.notif_status = True
		read_notif.save()
		return HttpResponse("add read notif success")
	return HttpResponse("add read notif not success")

def seenRemark(request):
	curr_patient = request.session['patient-uname-local']
	patient = Patient.objects.all().get(username=curr_patient)

	viewed_type = request.POST.get("viewed_type", "")	
	viewed_parent_pk = request.POST.get("file_pk", "")
	remark_type = request.POST.get("type", "")

	if remark_type == "notif":
		notif_pk = request.POST.get("notif_pk", "")
		if notif_pk is not None:
			for notif in patient.patient_new_notifications.all():
				if notif.pk == notif_pk:
					notif_root = patient.patient_notifications.all.get(pk=notif_pk)
					notif_root.status = False # change to notif status as old
					notif.save()
					patient.patient_new_notifications.remove(notif)  # remove in new notifications

	# mark viewed for every type of file
	if viewed_type == "Medical History Remark":
		for remark in patient.medical_history.latest().doctor_remarks.all():
			if remark.remark_seen == False:
				remark.remark_seen = True
				remark.seen_date = datetime.now()
				remark.save()
	elif viewed_type == "ICR Form Remark":
		for remark in patient.icr.doctor_remarks.all():
			if remark.remark_seen == False:
				remark.remark_seen = True
				remark.seen_date = datetime.now()
				remark.save()
	elif viewed_type == "Profile Form Remark":
		for remark in patient.profile.doctor_remarks.all():
			if remark.remark_seen == False:
				remark.remark_seen = True
				remark.seen_date = datetime.now()
				remark.save()
	elif viewed_type == "Consultation Schedule Remark":
		schedule = DoctorSchedule.objects.all().get(pk=viewed_parent_pk)
		for remark in schedule.doc_remark.all():
			if remark.remark_seen == False:
				remark.remark_seen = True
				remark.seen_date = datetime.now()
				remark.save()
	elif viewed_type == "Personal Record Comment":
		record = patient.personal_records.all().get(pk=viewed_parent_pk)
		for remark in record.comment.all():
			if remark.remark_seen == False:
				remark.remark_seen = True
				remark.seen_date = datetime.now()
				remark.save()
	return HttpResponse('success on contact')

def addPendingSched(request):
	curr_patient = request.session['patient-uname-local']
	curr_doctor = request.POST.get("curr_sched_doc", "")
	topic = request.POST.get("consultation_topic", "")
	date = request.POST.get("consultation_date", "")
	time = request.POST.get("consultation_time", "")
	notes = request.POST.get("consultation_notes", "")
	doctor = Doctor.objects.all().get(name=curr_doctor)
	patient = Patient.objects.all().get(username=curr_patient)

	if Patient.objects.all().filter(username=curr_patient).exists() and Doctor.objects.all().filter(name=curr_doctor).exists():
		
		new_pending_sched = DoctorSchedule()
		new_pending_sched.patient_username = curr_patient # firstname pa ang gi fees sa localhost
		new_pending_sched.doc_in_charge = curr_doctor
		c_date = date
		c_time = time
		c_datetime_str = c_date + " " + c_time
		new_pending_sched.schedule_date = datetime.strptime(c_datetime_str, '%Y-%m-%d %H:%M')

		new_pending_sched.schedule_topic = topic
		new_pending_sched.schedule_notes = notes
		new_pending_sched.patient_hiv_status = patient.HIV_status
		new_pending_sched.status = "pending"
		new_pending_sched.save()
		# to avoid adding identical schedule on refresh page
		if not patient.pending_schedules.all().filter(doc_in_charge = curr_doctor, schedule_date=new_pending_sched.schedule_date, patient_username = new_pending_sched.patient_username, schedule_topic=new_pending_sched.schedule_topic).exists():
			# add to patient's pending sched
			
			patient.pending_schedules.add(new_pending_sched)
			
			patient.save()
			# add to doctor's pending sched
			doctor.pending_scheds.add(new_pending_sched)


			doc_notif = DoctorNotification()
			doc_notif.name = curr_doctor
			doc_notif.patient_username = curr_patient
			doc_notif.subject = "Appointment"
			doc_notif.notif = curr_patient + " requested a consultation schedule with you."  #decline or accept
			doc_notif.user_type = "Patient"
			doc_notif.action_type = "Schedule Request"
			doc_notif.action_pk = new_pending_sched.pk
			doc_notif.created_on = datetime.now()
			doc_notif.save()
			doctor.doctorNotifs.add(doc_notif)
			doctor.save()

		all_doctors = Doctor.objects.all()
		p_message = "welcome"
		context={
			'p_message' : p_message,
			'patient' :  patient,
			'doctors': all_doctors,
		}
		return HttpResponse("Send Consultation Schedule Request Done.")
	return render(request, 'patient/patient.html')



def createNewPersonalRecord(request):
	curr_user = request.session['patient-uname-local']
	patient = Patient.objects.get(username=curr_user)
	new_record = PersonalRecord()
	author = curr_user
	title= request.POST.get("record_title", "")
	content = request.POST.get("record_content", "")
	rec_slug = (request.POST.get("record_title","")).replace(" ", "").lower() #use "" instead of "-" to avoid problems when using slug as part of id in doctors part
	# if same author, title, content, don't make one. pop up warning
	with_author = False
	with_title = False
	with_content = False
	
	if len(author) > 0:
		with_author = True
		new_record.author = author
	if len(title) > 0:
		with_title=True
		new_record.title  = title
	if len(content) > 0:
		with_content = True
		new_record.content  = content
	if len(rec_slug) > 0:
		new_record.slug = rec_slug
	if with_author and with_content and with_title:
		new_record.save()				
		patient.personal_records.add(new_record)
		patient.save()
		return HttpResponse("new record created!")
	return HttpResponse("new record cannot be created!")

# updates the patient details
# updates some ICR info
# updates the patient location details table , create a new location detail ONLY if present address is edited
def editAccInfo(request):
	# change location details to one to many rel
	icr_flag = False 
	loc_flag = False
	curr_patient = request.session['patient-uname-local']

	f_name = request.POST.get('f_name', "")
	s_name = request.POST.get('s_name', "")
	age = request.POST.get('age', "")
	bdate = request.POST.get('bdate', "")
	cellphone_num = request.POST.get('cellphone_num', "")
	email = request.POST.get('email', "")
	home_add = request.POST.get('home_add', "")
	present_add = request.POST.get('present_add', "")
	occ = request.POST.get('occ', "")
	work_add = request.POST.get('work_add', "")
	username = request.POST.get('username', "")
	password = request.POST.get('password', "")
	lat = request.POST.get('lat', "")
	lon = request.POST.get('lon', "")

	if Patient.objects.filter(username=curr_patient).exists():

		patient = Patient.objects.get(username=curr_patient)
		new_loc = patient.location_details.latest() #update the latest location detail for changes not related to present address		
		
		if len(f_name) > 0 or len(s_name) > 0:
			icr_flag = True
			loc_flag = True
			if f_name != patient.first_name and len(f_name) > 0:
				patient.first_name = f_name.lower()
				patient.icr.first_name = patient.first_name
			if s_name != patient.last_name and len(s_name) > 0:
				patient.last_name = s_name.lower()
				patient.icr.last_name = patient.last_name
			
			new_loc.patient_name = patient.first_name + " " + patient.last_name # update the location details

			patient.icr.save()

		if len(present_add) > 0:
			if present_add != patient.present_address:
				loc_flag = True
				# create a new location detail since a new address is given
				new_loc = PatientLocationDetails.objects.create()

				patient.present_address = present_add # update the patient present add
				
				if len(lat) > 0 and patient.location_details.latest().lat != lat:
					new_loc.lat = lat

				if len(lon) > 0 and patient.location_details.latest().lon != lon:
					new_loc.lon = lon
				
				if PatientLocationDetails.objects.all().filter(lat=lat, lon=lon).exists():
					new_loc.lon = str(float(new_loc.lon) + 0.001) #add .001 to create only unique locations
				
				
				new_loc.created_on = datetime.now()
				new_loc.location = present_add
				new_loc.work = patient.location_details.latest().work
				new_loc.patient_name = patient.location_details.latest().patient_name
				new_loc.username = patient.location_details.latest().username
				new_loc.hiv_level = patient.location_details.latest().hiv_level

				# send notif that present address is changed
				for doctor in patient.my_doctors.all():
					doc_notif = DoctorNotification()
					doc_notif.name = doctor.name
					doc_notif.patient_username = curr_patient
					doc_notif.subject = "Present Address"
					doc_notif.notif = curr_patient + " changed the present address to " + new_loc.location
					doc_notif.user_type = "Patient"
					doc_notif.action_type = "Edit"
					doc_notif.action_pk = new_loc.pk
					doc_notif.created_on = datetime.now()
					doc_notif.save()
					doctor.doctorNotifs.add(doc_notif)
					doctor.save()

		if len(username) > 0:
			if username != patient.username:
				loc_flag = True
				patient.username = username.lower() # extra check, must be lower
				new_loc.username = patient.username # update the location details
				

		if len(age) > 0:
			if age != patient.age:
				icr_flag = True
				patient.age = age
				patient.icr.age = patient.age
				patient.icr.save()

		if len(bdate) > 0:
			if bdate != patient.birthdate:
				icr_flag = True
				patient.birthdate = bdate
				patient.icr.birthdate = patient.birthdate
				patient.icr.save()

		if len(cellphone_num) > 0:
			if cellphone_num != patient.call_number:
				icr_flag = True
				patient.call_number = cellphone_num
				patient.icr.phone_number = patient.call_number
				patient.icr.save()

		if len(email) > 0:
			if email != patient.email:
				patient.email = email
		if len(home_add) > 0:
			if home_add != patient.home_address:
				icr_flag = True
				patient.home_address = home_add
				patient.icr.home_address = patient.home_address
				patient.icr.save()
		
		if len(occ) > 0:
			if occ != patient.work:
				icr_flag = True
				loc_flag = True
				patient.work = occ
				new_loc.work = occ
				patient.icr.occupation = patient.work
				patient.icr.save()
				
		if len(work_add) > 0:
			if work_add != patient.work_address:
				icr_flag = True
				patient.work_address = work_add
				patient.icr.work_address = patient.work_address
				patient.icr.save()
				
		if len(password) > 0:
			if password != patient.password:
				patient.password = password

		# send notif to doctors if patient edited his/her ICR info
		if icr_flag is True:
			for doctor in patient.my_doctors.all():
				doc_notif = DoctorNotification()
				doc_notif.name = doctor.name
				doc_notif.patient_username = curr_patient
				doc_notif.subject = "ICR Form"
				doc_notif.notif = curr_patient + " edited on Individual Client Record"
				doc_notif.user_type = "Patient"
				doc_notif.action_type = "Edit"
				doc_notif.action_pk = patient.icr.pk
				doc_notif.created_on = datetime.now()
				doc_notif.save()
				doctor.doctorNotifs.add(doc_notif)
				doctor.save()
		if loc_flag is True:
			new_loc.save()
			patient.location_details.add(new_loc)
		patient.save()
		return HttpResponse("Account Information Edited!")
	return HttpResponse("Account Information Not Edited!")

def editICR(request):

	curr_user = request.session['patient-uname-local']
	patient = Patient.objects.get(username=curr_user)

	fname = request.POST.get("first_name", "")
	last_name = request.POST.get("surname", "")
	middle_initial = request.POST.get("middle_name", "")
	sex = request.POST.get("sex", "")
	civil_status = request.POST.get("civil_status", "")
	home_add = request.POST.get("home_add", "")
	occupation = request.POST.get("occupation", "")
	work_add = request.POST.get("work_add", "")
	symptoms = request.POST.get("symptoms", "")
	specs = request.POST.get("specs", "")
	visit_date = request.POST.get("visit_date", "")
	age = request.POST.get("age", "")
	bdate = request.POST.get("bdate", "")
	phone_num = request.POST.get("phone_num", "")
	work_num = request.POST.get("work_num", "")
	visit_purpose_choice = request.POST.get("visit_purpose_choice", "") #exempt this ?? 

	if Patient.objects.filter(username=curr_user).exists():

		if len(fname) > 0:
			patient.icr.first_name = fname.lower().title()
		if len(last_name) > 0:
			patient.icr.last_name = last_name.lower().title()
		if len(middle_initial) > 0:
			patient.icr.middle_name = middle_initial.lower().title()
		if len(sex) > 0:
			patient.icr.sex = sex.lower()
		if len(civil_status)  > 0:
			patient.icr.civil_status = civil_status.lower().title()
		if len(home_add) > 0:		
			patient.icr.home_address = home_add.lower().title()
		if len(occupation) > 0:
			patient.icr.occupation = occupation.lower().title()
		if len(work_add) > 0:
			patient.icr.work_address = work_add.lower().title()
		if len(specs) > 0:
			patient.icr.specification = specs.lower()
		if len(symptoms) > 0:
			patient.icr.symptoms = symptoms.lower()
		if len(visit_purpose_choice) > 0:
			patient.icr.purpose_of_visit =  visit_purpose_choice
			print( visit_purpose_choice, "-"*50)

		if len(visit_date) > 0:
			patient.icr.date_of_visit = visit_date
		if len(age) > 0:
			patient.icr.age = age
		if len(bdate) > 0:
			patient.icr.birthdate = bdate
		if len(phone_num) > 0:
			patient.icr.phone_number = phone_num
		if len(work_num) > 0:
			patient.icr.work_number = work_num
		
		
		patient.icr.save()
		patient.pk = patient.icr.pk
		patient.save()

		for doctor in patient.my_doctors.all():
			doc_notif = DoctorNotification()
			doc_notif.name = doctor.name
			doc_notif.patient_username = curr_user
			doc_notif.subject = "ICR Form"
			doc_notif.notif = curr_user + " edited the ICR Form."
			doc_notif.user_type = "Patient"
			doc_notif.action_type = "Edit"
			doc_notif.action_pk = patient.icr.pk
			doc_notif.created_on = datetime.now()
			doc_notif.save()
			doctor.doctorNotifs.add(doc_notif)
			doctor.save()

		return HttpResponse('ICR Form edit done!')
	return render('ICR Form edit not done!')

def addDr(request): # add doctor/s from the list of doctors but still under pending list unless approved by admin
			
	docsChosen = request.POST.getlist('docs[]', "")
	doctors = Doctor.objects.all()
	curr_user = request.session['patient-uname-local']
	get_user = Patient.objects.all().filter(username=curr_user)
	patient = Patient.objects.get(username=curr_user)
	if len(docsChosen) > 0:
		for doctor in docsChosen:
			doc_exists = doctors.filter(name=doctor).exists()
			if doc_exists:
				new_doctor = Doctor.objects.get(name=doctor)
				# send a notif to the doctor 
				patient.my_doctors.add(new_doctor)			# for development purposes only 
				new_notif = DoctorNotification() 			# add to pending doctors and send to 
				new_notif.user_type = "Patient"
				new_notif.action_type = "New Patient"
				new_notif.action_pk = patient.pk
				new_notif.name = new_doctor.name 			# for documentation purposes in admin 
				new_notif.subject = "Patient"
				new_notif.patient_username = curr_user
				new_notif.notif = curr_user + " added you, " + new_doctor.name + " as a personal doctor."
				new_notif.created_on = datetime.now()
				new_notif.save()

				new_doctor.doctorNotifs.add(new_notif)

				# update doctor's stats
				# if there are still no monthly stats or its another year
				if new_doctor.p_handled_stats.monthly_stats.all().count() == 0 or any(x.created_on.year == new_notif.created_on.year for x in new_doctor.p_handled_stats.monthly_stats.all()) == False:
					monthly_stat = MonthlyStatistics()
				else:
					monthly_stat = new_doctor.p_handled_stats.monthly_stats.all().latest()
					monthly_stat.pk = MonthlyStatistics.objects.latest().pk + 1 # add 1 to create a new instance of monthly stat with the same data but diff key
				
				monthly_stat.doctor_name = new_doctor.name
				monthly_stat.created_on = datetime.now()
				monthly_stat.doc_pk = new_doctor.pk
				monthly_stat.year = new_notif.created_on.year
				monthly_stat.patient_pk = new_notif.action_pk 
				monthly_stat.year = new_notif.created_on.year

				if new_notif.created_on.month == 1:
					monthly_stat.january+=1
				elif new_notif.created_on.month == 2:
					monthly_stat.february+=1
				elif new_notif.created_on.month == 3:
					monthly_stat.march+=1
				elif new_notif.created_on.month == 4:
					monthly_stat.april+=1
				elif new_notif.created_on.month == 5:
					monthly_stat.may+=1
				elif new_notif.created_on.month == 6:
					monthly_stat.june+=1
				elif new_notif.created_on.month == 7:
					monthly_stat.july+=1
				elif new_notif.created_on.month == 8:
					monthly_stat.august+=1
				elif new_notif.created_on.month == 9:
					monthly_stat.september+=1
				elif new_notif.created_on.month == 10:
					monthly_stat.october+=1
				elif new_notif.created_on.month == 11:
					monthly_stat.november+=1
				elif new_notif.created_on.month == 12:
					monthly_stat.december+=1
				monthly_stat.save()

				new_doctor.p_handled_stats.monthly_stats.add(monthly_stat)
				new_doctor.save()

				patient.save()
				return HttpResponse("add doctor done")

			
	return HttpResponse("add doctor not done")

def removeDr(request): # remove doctor/s from the doctors list of patient user
	
	docsChosen = request.POST.getlist('docs[]', "")
	curr_user = request.session['patient-uname-local']
	patient = Patient.objects.get(username=curr_user)

	if Patient.objects.all().filter(username=curr_user).exists():	
		if (len(docsChosen) > 0):							
			for doc in docsChosen:
				doctor = Doctor.objects.all().get(name=doc)
				
				# send notif to doctor
				doc_notif = DoctorNotification()
				doc_notif.name = doctor.name
				doc_notif.patient_username = curr_user
				doc_notif.user_type = "Patient"
				doc_notif.action_type = "Removed"
				doc_notif.action_pk = patient.pk
				doc_notif.notif = curr_user + " removed you from his/her Doctors List."
				doc_notif.subject = "Patient"
				doc_notif.created_on = datetime.now()
				doc_notif.save()

				doctor.doctorNotifs.add(doc_notif)

				#  manually update monthly stat
				if doctor.p_handled_stats.monthly_stats.all().count() == 0 or any(x.created_on.year == doc_notif.created_on.year for x in doctor.p_handled_stats.monthly_stats.all()) == False:
					monthly_stat = MonthlyStatistics()
				else:
					monthly_stat = doctor.p_handled_stats.monthly_stats.all().latest()
					monthly_stat.pk = MonthlyStatistics.objects.latest().pk + 1 # add 1 to create a new instance of monthly stat with the same data but diff key
					monthly_stat.created_on = datetime.now()
				if doc_notif.created_on.month == 1:
					monthly_stat.january-=1
				elif doc_notif.created_on.month == 2:
					monthly_stat.february-=1
				elif doc_notif.created_on.month == 3:
					monthly_stat.march-=1
				elif doc_notif.created_on.month == 4:
					monthly_stat.april-=1
				elif doc_notif.created_on.month == 5:
					monthly_stat.may-=1
				elif doc_notif.created_on.month == 6:
					monthly_stat.june-=1
				elif doc_notif.created_on.month == 7:
					monthly_stat.july-=1
				elif doc_notif.created_on.month == 8:
					monthly_stat.august-=1
				elif doc_notif.created_on.month == 9:
					monthly_stat.september-=1
				elif doc_notif.created_on.month == 10:
					monthly_stat.october-=1
				elif doc_notif.created_on.month == 11:
					monthly_stat.november-=1
				elif doc_notif.created_on.month == 12:
					monthly_stat.december-=1
				monthly_stat.save()

				doctor.p_handled_stats.monthly_stats.add(monthly_stat)


				doctor.save()

				patient.my_doctors.remove(doctor)
				return HttpResponse("remove done!")
	return HttpResponse("remove done!")
