from django.shortcuts import render
from django.http import HttpResponse
from patient.models import Patient, PatientNotification, MedHistForm, Medication
from cebuMap.models import CebuBarangays 

from .models import Doctor, Remark, UsersViewed, DoctorSchedule, Medicine, DoctorNotification
import os
from datetime import datetime, date
from django.contrib.gis.geos import Point
#from django.views.decorators.cache import cache_control

# log out doctor
#@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def docLogout(request):
	try:
		doc_name = request.session['doc-name-local']
		doctor = Doctor.objects.all().get(name=doc_name)
		doctor.new_notifs.clear()  # prevent resetting last log put on  page refresh
		if doctor.login_flag is True:
			doctor.last_log_out = datetime.now()
			doctor.login_flag=False
		doctor.save()
		request.session['doc-name-local'] = None
	except:
		print("no more stored data in session storage")
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
			doc_name = request.session['doc-name-local']
			doctor = Doctor.objects.all().get(name=doc_name)
			image = request.FILES.get('image')
			doctor.doc_image.delete(save=True) # save=True to still save the model instance without the prev url
			doctor.doc_image = image
			doctor.save()
			return HttpResponse("upload patient profile picture success!")
	return HttpResponse("upload patient profile picture not success.")



def addMeds(request):

	meds_list = request.POST.getlist('new_meds[]') #array of med pk
	curr_patient = request.POST.get('curr_patient')
	notes = request.POST.get('notes', "")
	doc_name = request.session['doc-name-local']
	if Patient.objects.all().filter(username=curr_patient).exists():
		patient= Patient.objects.all().get(username=curr_patient)
		for med in meds_list:
			if Medicine.objects.all().filter(pk=med).exists():
				medicine = Medicine.objects.all().get(pk=med)
				
				# add new med to patient
				patient_med = Medication()
				patient_med.created_on = datetime.now()
				patient_med.patient_pk = patient.pk
				patient_med.username = patient.username

				patient_med.drug_group = medicine.drug_group
				patient_med.drug_name = medicine.drug_name
				patient_med.medicine_type = medicine.medicine_type
				patient_med.unit_of_measure = medicine.unit_of_measure
				patient_med.content_per_bottle = medicine.content_per_bottle

				patient_med.administered_by = doc_name
				patient_med.doc_notes = notes
				patient_med.save()

				patient.meds.add(patient_med)

				# notify the patient
				notif = PatientNotification()
				notif.patient_username = curr_patient
				notif.doctor_name = doc_name
				notif.user_type = "Doctor"
				notif.action_type="Add"
				notif.notification = "Dr. " + doc_name + " added a New Medication on your ART Medications"
				notif.subject = "ART Medication"
				notif.action_pk = patient_med.pk
				notif.created_on = datetime.now()
				notif.status = True
				notif.save()

				patient.patient_notifications.add(notif)

				patient.save()
				
				return HttpResponse("Add new meds done!!")


	return HttpResponse("Add new meds not done!!")

def notifRead(request):

	notif_pk = request.POST.get("notif_pk","")
	if DoctorNotification.objects.all().filter(pk=notif_pk).exists():
		read_notif = DoctorNotification.objects.all().get(pk=notif_pk)

		read_notif.notif_status = True
		read_notif.save()
		return HttpResponse("add read notif success")
	return HttpResponse("add read notif not success")


# doesn't show in the /addSeen page but well done in admin 
def addSeenDoc(request):
	doc_name = request.session['doc-name-local']
	file_owner = request.POST.get("file_owner", "")
	file_pk = request.POST.get("file_pk", "")
	viewed_type = request.POST.get("viewed_type", "")
	if Patient.objects.all().filter(username=file_owner).exists():

		patient = Patient.objects.all().get(username=file_owner)
		new_view = UsersViewed()
		new_view.seen_date = datetime.now()
		new_view.seen_flag = True
		new_view.viewer_type = "Doctor"
		new_view.viewer_name = doc_name
		new_view.viewed_pk = file_pk
		new_view.file_owner = file_owner
		if PatientNotification.objects.all().filter(pk=file_pk).exists():
			notif = PatientNotification.objects.all().get(pk=file_pk)
			notif.notif_status = True

		if viewed_type == "Personal Record":
			new_view.viewed_type = "Personal Record"
			if patient.personal_records.all().filter(pk=file_pk).exists():
				record = patient.personal_records.all().get(pk=file_pk)
				if not record.docs_viewed.all().filter(viewer_name = doc_name, viewed_pk=file_pk).exists():
					new_view.save()
					record.docs_viewed.add(new_view)
					record.save()
					return HttpResponse('success!') # only used for clarity's sake

		elif viewed_type == "Consultation Schedule":    # viewed by doctor scheduled for appointment and patient who requested it
			new_view.viewed_type = "Consultation Schedule"
			if DoctorSchedule.objects.all().filter(pk=file_pk).exists():
				
				schedule = DoctorSchedule.objects.all().get(pk=file_pk)
				if not schedule.users_viewed.all().filter(viewer_name=doc_name).exists():
					new_view.save()
					schedule.users_viewed.add(new_view)
					schedule.save()
					return HttpResponse("consultation schedule success!")
		elif viewed_type == "ICR":
			new_view.viewed_type="ICR"
			if Patient.objects.all().filter(username=file_owner).exists():
				
				patient = Patient.objects.all().get(username=file_owner)
				if not patient.icr.docs_viewed.all().filter(viewer_name=doc_name).exists():
					new_view.save()
					patient.icr.docs_viewed.add(new_view)
					patient.icr.save()
					patient.save()
					return HttpResponse("ICR success!")
		#elif viewed_type == "Profile Form":
		#	new_view.viewed_type="Profile Form"
		#	if Patient.objects.all().filter(username=file_owner).exists():
		#		
		#		patient = Patient.objects.all().get(username=file_owner)
		#		if not patient.profile.docs_viewed.all().filter(viewer_name=doc_name).exists():
		#			new_view.save()
		#			patient.profile.docs_viewed.add(new_view)
		#			patient.profile.save()
		#			patient.save()
		#			return HttpResponse("Profile Form success!")
		elif viewed_type == "Medical History":
			new_view.viewed_type="Medical History"
			if Patient.objects.all().filter(username=file_owner).exists():
				
				patient = Patient.objects.all().get(username=file_owner)
				if not patient.medical_history.latest().docs_viewed.all().filter(viewer_name=doc_name).exists(): # add seen action to the latest medhist 
					new_view.save()
					patient.medical_history.latest().docs_viewed.add(new_view)
					patient.medical_history.latest().save()
					patient.save()
					return HttpResponse("Medical History success!")
		
	return HttpResponse('not success')


# updates the status of the patient: (1)ongoing therapy, (2)outside cebu, (3)deaceased, (4) withing cebu
def docUpdatePStat(request):
	curr_doctor = request.session['doc-name-local']
	doctor = Doctor.objects.all().get(name=curr_doctor)

	new_status = request.POST.get("p_stat", "")
	patient_pk = request.POST.get("patient_pk", "")
	patient_add = request.POST.get("patient_add", "") # changeable
	patient_gen_loc = request.POST.get("patient_gen_loc", "")

	if Patient.objects.all().filter(pk=patient_pk).exists(): 
		patient = Patient.objects.all().get(pk=patient_pk)
		prev_status = patient.status
		if patient_gen_loc != "":
			patient_loc = patient.location_details.latest()
			patient_loc.general_location = patient_gen_loc
			patient_loc.save()

			# notify the patient for changes
			notif = PatientNotification()
			notif.patient_username = patient.username
			notif.doctor_name = curr_doctor
			notif.user_type = "Doctor"
			notif.action_type = "Change"
			notif.notification = "Dr. "+ curr_doctor + " changed your location to " + new_status + "."
			notif.subject="Profile"
			notif.action_pk = patient.pk
			notif.created_on = datetime.now()
			notif.status = True
			notif.save()

			patient.patient_notifications.add(notif)
			patient.save()

		if new_status!="":
			patient.status = new_status
			update_loc = patient.location_details.latest()
			update_loc.status = new_status # update location details - what patient data can be seen in map
			update_loc.save()
			
			# notify the patient for changes
			notif = PatientNotification()
			notif.patient_username = patient.username
			notif.doctor_name = curr_doctor
			notif.user_type = "Doctor"
			notif.action_type = "Change"
			notif.notification = "Dr. "+ curr_doctor + " changed your status to " + new_status + "."
			notif.subject="Profile"
			notif.action_pk = patient.pk
			notif.created_on = datetime.now()
			notif.status = True
			notif.save()

			patient.patient_notifications.add(notif)
			patient.save()

			# update the brgy on change status of patient 
			patient_point = Point(float(patient.location_details.latest().lon), float(patient.location_details.latest().lat))
			if CebuBarangays.objects.filter(geom__intersects=patient_point).exists():
				brgy = CebuBarangays.objects.get(geom__intersects=patient_point)
					
				# add patient to the new status's table in brgy
				if new_status == "outside cebu":
					brgy.migrated.add(patient)
				elif new_status == 'deceased':
					brgy.deceased.add(patient)
				
				# remove patient from prev status's table in brgy
				if prev_status == "outside cebu":
					if brgy.migrated.all().filter(pk=patient.pk).exists():
						brgy.migrated.remove(patient)
				elif prev_status == 'deceased':
					if brgy.deceased.all().filter(pk=patient.pk).exists():
						brgy.deceased.remove(patient)				
				brgy.save()
		return HttpResponse("update patient status done.")
	return HttpResponse("update patient status not done.")

def docEditICR(request):

	curr_doctor = request.session['doc-name-local']
	doctor = Doctor.objects.all().get(name=curr_doctor)

	curr_patient = request.POST.get("patient_icr_uname")

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
	visit_date = request.POST.get("visit_date")
	age = request.POST.get("age")
	bdate = request.POST.get("bdate")
	phone_num = request.POST.get("phone_num")
	work_num = request.POST.get("work_num")
	visit_purpose = request.POST.get("visit_purpose") 
	p_remark = request.POST.get("remark")

	if Patient.objects.all().filter(username=curr_patient).exists():
		patient = Patient.objects.get(username=curr_patient)
		if len(fname) > 0:
			patient.icr.first_name = fname.lower()
		if len(last_name) > 0:
			patient.icr.last_name = last_name.lower()
		if len(middle_initial) > 0:
			patient.icr.middle_name = middle_initial.lower()
		if len(sex) > 0:
			patient.icr.sex = sex.lower()
		if len(civil_status)  > 0:
			patient.icr.civil_status = civil_status.lower()
		if len(home_add) > 0:		
			patient.icr.home_address = home_add.lower()
		if len(occupation) > 0:
			patient.icr.occupation = occupation.lower()
		if len(work_add) > 0:
			patient.icr.work_address = work_add.lower()
		if len(specs) > 0:
			patient.icr.specification = specs.lower()
		if len(symptoms) > 0:
			patient.icr.symptoms = symptoms.lower()
		if visit_date != None:
			patient.icr.date_of_visit = visit_date
		if age != None:
			patient.icr.age = age
		if bdate != None:
			patient.icr.birthdate = bdate
		if phone_num != None:
			patient.icr.phone_number = phone_num
		if work_num != None:
			patient.icr.work_number = work_num
		if len(visit_purpose) > 0:
			patient.icr.purpose_of_visit = visit_purpose #exempt this
		patient.icr.save()

		if len(p_remark) > 0:
			remark = p_remark		
#		if len(remark) > 0:
			new_remark =  Remark()
			new_remark.author = curr_doctor
			new_remark.text = remark
			new_remark.remark_parent_type = "ICR Form"
			new_remark.remark_receiver = patient.username
			new_remark.save()
			patient.icr.doctor_remarks.add(new_remark)

			# send notif to patient that that a remark has been made
			notif = PatientNotification()
			notif.patient_username = curr_patient
			notif.doctor_name = curr_doctor
			notif.user_type = "Doctor"
			notif.action_type = "Remark"
			notif.notification = "Dr. " + curr_doctor + " added a remark on your Individual Client Form."
			notif.subject = "ICR"
			notif.action_pk = patient.pk
			notif.created_on = datetime.now()
			notif.status = True
			notif.save()
			patient.patient_notifications.add(notif)
			patient.icr.doctor_remarks.add(new_remark)
	
		# notify the patient for changes
		notif = PatientNotification()
		notif.patient_username = curr_patient
		notif.doctor_name = curr_doctor
		notif.user_type = "Doctor"
		notif.action_type = "Edit"
		notif.notification = "Dr. "+ curr_doctor + " edited your Individual Client Form."
		notif.subject="ICR"
		notif.action_pk = patient.pk
		notif.created_on = datetime.now()
		notif.status = True
		notif.save()
		patient.patient_notifications.add(notif)

		patient.icr.save()
		patient.pk = patient.icr.pk
		patient.save()
		patients=Patient.objects.all()
		patient_arr=[]
		for p in patients:
			if p.my_doctors.filter(name=curr_doctor).exists():
				patient_arr.append(p) 

		p_message = "welcome"
		context={
			'p_message' : p_message,
			'doctor' : doctor,
			'patients': patient_arr,
		}
		print("ICR Form success")
		return render(request, 'doctor/doctor.html',  context)
	return render(request, 'doctor/doctor.html')	

def docEditMedHist(request):
	send_notif = False
	change_hiv_level = False
	curr_doctor = request.session['doc-name-local']
	curr_patient = request.POST.get("uname", "")
	remark = request.POST.get("remark", "")
	patient = Patient.objects.all().get(username=curr_patient)
	
	med_hist = patient.medical_history.latest()  # get the latest created medhist
	prev_medhist = patient.medical_history.latest() 
	exposure = request.POST.get("exposure", "")
	other_med_con = request.POST.get("other_med_con", "")
	date_diagnosed = request.POST.get("date_diagnosed", "")
	hiv_level = request.POST.get("hiv_level", "")
	hiv_level_choice = request.POST.get("hiv_level_choice", "")

	if len(date_diagnosed) == 0:
		try:
			date_diagnosed = patient.medical_history.latest().date_diagnosed
		except:
			date_diagnosed = datetime.now()

	if not patient.medical_history.all().filter(username=curr_patient, exposure=exposure, other_conditions=other_med_con, date_diagnosed=date_diagnosed).exists():
		med_hist = MedHistForm.objects.create() # if medhist is edited then add new medhist

		med_hist.created_on = datetime.now()
		med_hist.parent_pk = patient.pk
		med_hist.username = patient.username


		if date_diagnosed is not None:
			med_hist.date_diagnosed = date_diagnosed
			send_notif = True
		else:
			send_notif = False
		if len(exposure) > 1:
			med_hist.exposure = exposure
			send_notif = True
		else:
			send_notif = False

		if len(other_med_con) > 1:
			med_hist.other_conditions = other_med_con
			send_notif = True
		else:
			send_notif = False
			
	if len(hiv_level_choice) > 0:
		prev_hiv_status = patient.HIV_status 
		patient.HIV_status = hiv_level_choice
		if hiv_level_choice.lower() == 'negative':
			med_hist.exposure = negative
		elif hiv_level_choice.lower() != 'for screening' or hiv_level_choice.lower() != 'negative':
			med_hist.exposure = "positive"
		
		details = patient.location_details.latest()
		details.hiv_level = patient.HIV_status
		details.save()
		
	else:
		# do nothing
		print("no choicee-------------------")

		
	med_hist.doctor_remarks.set(prev_medhist.doctor_remarks.all()) #copy the remarks of the previous medical history
	med_hist.docs_viewed.set(prev_medhist.docs_viewed.all()) #copy all the doctors who viewed

	# create an instance of remark
	new_remark =  Remark()
	new_remark.author = curr_doctor
	new_remark.text = remark
	new_remark.remark_parent_type = "Medical History Form"
	new_remark.remark_receiver = patient.username

	if len(remark) > 0:
		new_remark.save()
		med_hist.doctor_remarks.add(new_remark) #add the new remark to the new medhist

		# send notif to patient that that a remark has been made
		notif = PatientNotification()
		notif.patient_username = curr_patient
		notif.doctor_name = curr_doctor
		notif.user_type = "Doctor"
		notif.action_type = "Remark"
		notif.notification = "Dr. " + curr_doctor + " added a remark on your medical history"
		notif.subject = "Medical History"
		notif.action_pk = patient.pk
		notif.created_on = datetime.now()
		notif.status = True
		notif.save()
		patient.patient_notifications.add(notif)
		# med_hist.doctor_remarks.add(new_remark)

	med_hist.save()

	if not (patient.medical_history.all().filter(pk=med_hist.pk).exists()):
		patient.save()
		patient.medical_history.add(med_hist)  #if  medhist is new, save, else don't save again.otherwise, ends up w/ dups
	if send_notif is True:	
		# notify the patient for changes
		notif = PatientNotification()
		notif.patient_username = curr_patient
		notif.doctor_name = curr_doctor
		notif.user_type = "Doctor"
		notif.action_type = "Edit"
		notif.subject="Medical History"
		notif.action_pk = patient.pk
		notif.notification = "Dr. "+ curr_doctor + " edited your Medical History."
		notif.created_on = datetime.now()
		notif.status = True
		notif.save()
		patient.patient_notifications.add(notif)
	patient.save()

	patient_point = Point(float(patient.location_details.latest().lon), float(patient.location_details.latest().lat))
	if len(hiv_level_choice) > 0:
		print("change of hiv level------------------ \n exists: ", CebuBarangays.objects.filter(geom__intersects=patient_point).exists())
		
		change_hiv_level = True
		if CebuBarangays.objects.filter(geom__intersects=patient_point).exists():
			brgy = CebuBarangays.objects.get(geom__intersects=patient_point)
			print("---------location located: ",  brgy.name_3)

			if brgy.hiv_pop.all().filter(pk=patient.pk).exists():
				if prev_hiv_status == "stage 1":
					if brgy.stage_1.all().filter(pk=patient.pk).exists():
						brgy.stage_1.remove(patient)
				elif prev_hiv_status == "stage 2":
					if brgy.stage_2.all().filter(pk=patient.pk).exists():
						brgy.stage_2.remove(patient)
				elif prev_hiv_status == "stage 3":
					if brgy.stage_3.all().filter(pk=patient.pk).exists():
						brgy.stage_3.remove(patient)
				if brgy.hiv_pop.all().filter(pk=patient.pk).exists():
					rem_patient = brgy.hiv_pop.all().get(pk=patient.pk)
					brgy.hiv_pop.remove(patient)
			
			elif prev_hiv_status == "for screening":	
				if brgy.for_screening.all().filter(pk=patient.pk).exists():				
					brgy.for_screening.remove(patient)
			
			elif prev_hiv_status == "negative":
				if brgy.stage_0.all().filter(pk=patient.pk).exists():
					brgy.stage_0.remove(patient)			
			
			# add the patient to where it is stored based on changed HIV_status
			if patient.HIV_status == "for screening":
				brgy.for_screening.add(patient)
			elif patient.HIV_status == "negative":
				brgy.stage_0.add(patient)
			else:
				brgy.hiv_pop.add(patient)
				if patient.HIV_status == "stage 1":
					brgy.stage_1.add(patient)
				elif patient.HIV_status == "stage 2":
					brgy.stage_2.add(patient)
				elif patient.HIV_status == "stage 3":
					brgy.stage_3.add(patient)
			
			brgy.save()	
			
		if change_hiv_level:
			# notify the patient for changes
			notif = PatientNotification()
			notif.patient_username = curr_patient
			notif.doctor_name = curr_doctor
			notif.user_type = "Doctor"
			notif.action_type = "Edit"
			notif.subject="Medical History"
			notif.action_pk = patient.pk
			notif.notification = "Dr. "+ curr_doctor + " changed your HIV status."
			notif.created_on = datetime.now()
			notif.status = True
			notif.save()
			patient.patient_notifications.add(notif)
			patient.save()
	return HttpResponse("Edit Medical History Done")
		


# remark_type = (pending, accepted, rejected, finished)
# parent_pname = owner of the parent of the add remark modal
# parent_pk = pk of the Add A Remark Sender
# doc_remark = remark of doctor of type  Remark() 
def addARemark(request):
	# if request.method=="POST":	
	curr_doctor = request.session['doc-name-local']
	curr_patient = request.POST.get("p_sched_uname", "")
	parent_pk = request.POST.get("p_sched_pk", "")
	remark_type = request.POST.get("remark_type", "")
	doc_remark = request.POST.get("p_sched_remark", "")
	
	if Doctor.objects.all().filter(name=curr_doctor).exists() and Patient.objects.all().filter(username=curr_patient).exists():
		
		doctor = Doctor.objects.all().get(name=curr_doctor)
		patient = Patient.objects.all().get(username=curr_patient)

		#create the doctor's remark of type Remark	
		new_remark = Remark()
		new_remark.author = curr_doctor
		new_remark.text = doc_remark
		new_remark.remark_parent_type = "Consultation Schedule"
		new_remark.remark_receiver = patient.username
		new_remark.save()

		# check which parent database the remark falls into 
		remark_db = doctor.pending_scheds.all()
		if remark_type == "accepted":
			remark_db = doctor.schedules.all()
		elif remark_type == "rejected":
			remark_db = doctor.rejected_scheds.all()
		elif remark_type == "finished":
			remark_db = doctor.finished_scheds.all()

		action_type_adder = remark_type
		if action_type_adder == "rejected":
			action_tyoe_adder = "declined"
		# fetch the schedule designated object
		sched =  remark_db.get(patient_username=curr_patient, pk=parent_pk)
		if not sched.doc_remark.all().filter(author=new_remark.author, text=new_remark.text).exists():
			sched.doc_remark.add(new_remark)	# add a remark to the schedule
			sched.save()
			
			# initialize a notif
			notif = PatientNotification()
			notif.patient_username = curr_patient
			notif.doctor_name = curr_doctor
			notif.user_type = "Doctor"
			notif.action_type = "Remark" + " " + action_type_adder.title()
			notif.status = True
			
			# check for doctor names special case (2 first names e.g. anna marie) 
			if ' ' in curr_doctor:
				doc_fname, doc_lname = curr_doctor.split(' ', 1)
			else:
				doc_fname = curr_doctor
				doc_lname = ""

			# send notif to patient that that a remark has been made
			notif.notification = "Dr. " + doc_fname.capitalize() + " " + doc_lname.capitalize() + " remarked on your schedule:"+ os.linesep + sched.schedule_topic
			notif.subject = "Consultation Schedule"
			notif.action_pk = sched.pk
			notif.created_on = datetime.now()
			notif.save()

			patient.patient_notifications.add(notif)
			patient.save()

		return HttpResponse("add a remark done!")

	return render(request, 'doctor/doctor.html')


def finishSched(request):
	
	curr_doctor = request.session['doc-name-local']
	curr_patient = request.POST.get("o_sched_uname")
	sched_topic = request.POST.get("o_sched_topic")
	sched_pk = request.POST.get("o_sched_pk")
	created_on = request.POST.get("o_sched_created_on")
	
	if Doctor.objects.all().filter(name=curr_doctor).exists() and Patient.objects.all().filter(username=curr_patient).exists():
		
		doctor = Doctor.objects.all().get(name=curr_doctor)
		patient = Patient.objects.all().get(username=curr_patient)
		if doctor.schedules.all().filter(patient_username=curr_patient, schedule_topic=sched_topic).exists():

			sched =  doctor.schedules.all().get(patient_username=curr_patient, schedule_topic=sched_topic, pk=sched_pk)

			# initialize a notif
			notif = PatientNotification()
			notif.patient_username = curr_patient
			notif.doctor_name = curr_doctor
			notif.user_type = "Doctor"
			notif.action_type = "Finished"
			notif.action_taken = 3 # 2 means finished
			notif.status = True

			# check for doctor names special case (2 first names e.g. anna marie) 
			if ' ' in curr_doctor:
				doc_fname, doc_lname = curr_doctor.split(' ', 1)
			else:
				doc_fname = curr_doctor
				doc_lname = ""

			sched.status="finished"
			
			sched.save()
			doctor.schedules.remove(sched)
			doctor.finished_scheds.add(sched)
			doctor.save()

			if doctor.doctorNotifs.all().filter(action_pk = sched_pk, patient_username=curr_patient, action_type="Schedule Request").exists():
				edited_notif = doctor.doctorNotifs.all().get(action_pk = sched_pk, patient_username=curr_patient, action_type="Schedule Request")
				edited_notif.action_taken = 3
				edited_notif.save()

			# send notif to patient that sched is finished 
			notif.notification = "Dr. " + doc_fname.capitalize() + " " + doc_lname.capitalize() + " marked your schedule for consultation FINISHED."
			notif.subject = "Consultation Schedule"
			notif.action_pk = sched.pk
			notif.created_on = datetime.now()
			notif.save()
			
			patient.patient_notifications.add(notif)

			# add to patients finished scheds and remove to ongoing
			finished_sched = patient.approved_schedules.all().get(schedule_topic=sched_topic, pk=sched_pk)
			patient.approved_schedules.remove(finished_sched)
			patient.finished_schedules.add(finished_sched)

			patient.save()

		patients = Patient.objects.all()
		patient_arr=[]
		for p in patients:
			if p.my_doctors.filter(name=curr_doctor).exists():
				patient_arr.append(p) 
		
		p_message = "welcome"
		context={
			'p_message' : p_message,
			'doctor' : doctor,
			'patients': patient_arr,
		}
		return HttpResponse("Sched Finish Done!")
	return HttpResponse("FINISH CONSULTATION SCHED NOT DONE")


def acceptSched(request):	
	curr_doctor = request.session['doc-name-local']
	curr_patient = request.POST.get("p_sched_uname")
	sched_topic = request.POST.get("p_sched_topic", "")
	sched_pk = request.POST.get("p_sched_pk", "")
	sched_remark = request.POST.get("p_sched_remark", "")
	
	if Doctor.objects.all().filter(name=curr_doctor).exists() and Patient.objects.all().filter(username=curr_patient).exists():
		doctor = Doctor.objects.all().get(name=curr_doctor)
		patient = Patient.objects.all().get(username=curr_patient)
		if doctor.pending_scheds.all().filter(patient_username=curr_patient, pk=sched_pk, schedule_topic=sched_topic).exists():
			if not doctor.schedules.all().filter(pk=sched_pk).exists():
				sched =  doctor.pending_scheds.all().get(pk=sched_pk)
				sched.status="accepted"
				sched.save()

				doctor.removePendingSched(sched)
				

				if doctor.doctorNotifs.all().filter(action_pk = sched_pk).exists():
					edited_notif = doctor.doctorNotifs.all().get(action_pk = sched_pk)
					edited_notif.action_taken = 1
					edited_notif.save()

				if len(sched_remark) > 0:
					new_remark = Remark()
					new_remark.author = doctor.name
					new_remark.text = sched_remark
					new_remark.created_date = datetime.now()
					new_remark.remark_parent_type = "Consultation Schedule"
					new_remark.remark_receiver = patient.username
					new_remark.save()
					sched.doc_remark.add(new_remark)
				
				
				doctor.schedules.add(sched)
				
				doctor.save()

				# send notif to patient that sched is accepted
				notif = PatientNotification()
				notif.patient_username = curr_patient
				notif.doctor_name = curr_doctor
				notif.user_type = "Doctor"
				notif.action_type = "Accepted"
				notif.action_taken = 1 # number 1 means accepted
				notif.status = True
				
				if ' ' in curr_doctor:
					doc_fname, doc_lname = curr_doctor.split(' ', 1)
				else:
					doc_fname = curr_doctor
					doc_lname = ""
				
				notif.notification = "Dr. " + doc_fname.capitalize() + " " + doc_lname.capitalize() + " accepted your request to schedule a consultation."
				notif.subject = "Consultation Schedule"
				notif.action_pk = sched.pk
				notif.created_on = datetime.now()
				notif.save()
					
				patient.patient_notifications.add(notif)

				# add to patients accepted scheds and remove to pending
				if not patient.approved_schedules.all().filter(pk=sched_pk, schedule_topic = sched_topic).exists():
					accepted_sched = patient.pending_schedules.all().get(schedule_topic=sched_topic, pk=sched_pk)
					patient.pending_schedules.remove(accepted_sched)
					patient.approved_schedules.add(accepted_sched)
				patient.save()

		patients = Patient.objects.all()
		patient_arr=[]
		for p in patients:
			if p.my_doctors.filter(name=curr_doctor).exists():
				patient_arr.append(p) 
		
		p_message = "welcome"
		context={
			'p_message' : p_message,
			'doctor' : doctor,
			'patients': patient_arr,
		}
		return HttpResponse('accept sched done!')
	return HttpResponse("ACCEPT CONSULTATION SCHED NOT DONE")


def rejectSched(request):
	curr_doctor = request.session['doc-name-local']
	curr_patient = request.POST.get("r_sched_uname")
	sched_topic = request.POST.get("r_sched_topic")
	sched_created = request.POST.get("r_sched_created_on")
	sched_pk = request.POST.get("r_sched_pk")
	sched_remark = request.POST.get("r_sched_remark")
	
	if Doctor.objects.all().filter(name=curr_doctor).exists() and Patient.objects.all().filter(username=curr_patient).exists():
		patient = Patient.objects.all().get(username=curr_patient)
		doctor= Doctor.objects.all().get(name=curr_doctor)
		if doctor.pending_scheds.all().filter(schedule_topic = sched_topic, pk=sched_pk).exists():

			# save the remarks 
			new_remark = Remark()
			new_remark.author = curr_doctor
			new_remark.text = sched_remark
			new_remark.remark_parent_type = "Consultation Schedule"
			new_remark.remark_receiver = curr_patient
			new_remark.save()

			# change schedule status from pending to rejected
			doc_sched = doctor.pending_scheds.all().get(schedule_topic = sched_topic, pk=sched_pk)
			doctor.removePendingSched(doc_sched)
			doc_sched.status = "rejected"
			doc_sched.doc_remark.add(new_remark)
			doc_sched.save()

			doctor.rejected_scheds.add(doc_sched)
			doctor.save()
			
			if doctor.doctorNotifs.all().filter(action_pk = sched_pk).exists():
				edited_notif = doctor.doctorNotifs.all().get(action_pk = sched_pk)
				edited_notif.action_taken = 2
				edited_notif.save()

			# send notif to patient that sched is rejected 
			notif = PatientNotification()
			notif.patient_username = curr_patient
			notif.doctor_name = curr_doctor
			notif.user_type = "Doctor"
			notif.action_type = "Declined"
			notif.action_taken = 2 # 2 mean rejected
			notif.status = True
			
			if ' ' in curr_doctor:
				doc_fname, doc_lname = curr_doctor.split(' ', 1)
			else:
				doc_fname = curr_doctor
				doc_lname = ""
			
			notif.notification = "Dr. " + doc_fname.capitalize() + " " + doc_lname.capitalize() + " declined your request to schedule a consultation."
			notif.subject = "Consultation Schedule"
			notif.action_pk = doc_sched.pk
			notif.created_on = datetime.now()
			notif.save()
			
			patient.patient_notifications.add(notif)

			# add to patients rejected scheds and remove to pending
			rejected_sched = patient.pending_schedules.all().get(schedule_topic = sched_topic, pk=sched_pk)
			patient.pending_schedules.remove(rejected_sched)
			patient.rejected_schedules.add(rejected_sched)
			patient.save()
			

		patient_arr = []
		patients = Patient.objects.all()
		for p in patients:
			if p.my_doctors.filter(name=curr_doctor).exists():
				patient_arr.append(p) 
		
		p_message = "welcome"
		context={
			'p_message' : p_message,
			'doctor' : doctor,
			'patients': patient_arr,
		}
		return HttpResponse("Declined Consultation Done!")
	return HttpResponse("REJECT CONSULTATION SCHED NOT DONE")



# add a comment in personal records
def addComment(request):

	curr_doctor = request.session['doc-name-local']
	patient_uname = request.POST.get("record_patient_username", "")
	curr_record_slug = request.POST.get("record_patient_slug", "")
	patient = Patient.objects.all().get(username=patient_uname)
	curr_text = request.POST.get("new_comment", "")
	doctor = Doctor.objects.all().get(name=curr_doctor)
	if len(curr_text) > 0:
		for record in patient.personal_records.all():
			if record.slug == curr_record_slug:
				
				new_comment = Remark()
				new_comment.author = curr_doctor
				new_comment.text = curr_text
				new_comment.remark_parent_type = "Personal Record"
				new_comment.remark_receiver = patient.username
				
				if not (record.comment.all().filter(author=new_comment.author, text=new_comment.text).exists()): 
					# add a notif
					notif = PatientNotification()
					notif.patient_username = patient_uname
					notif.doctor_name = curr_doctor
					notif.user_type = "Doctor"
					notif.action_type = "Comment"
					notif.subject = "Personal Record"
					notif.action_pk = record.pk 
					notif.notification = "Dr. "+ curr_doctor + " added a comment in your Daily Record: " + record.title
					notif.created_on = datetime.now()
					notif.status = True
					notif.save()
					patient.patient_notifications.add(notif)
					
					# save new comment
					new_comment.created_date = datetime.now()
					new_comment.save()
					record.comment.add(new_comment)		
		return HttpResponse("add comment done!")
	return HttpResponse("ADD COMMENT NOT DONE")



			



	





