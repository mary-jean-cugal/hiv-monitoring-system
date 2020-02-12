from django.contrib import admin
from django.contrib.auth.models import User, Group

from leaflet.admin import LeafletGeoAdmin
from django.utils.html import format_html

from patient.models import Patient, ICRForm, ProfileForm, MedHistForm, PatientNotification, PersonalRecord, PatientLocationDetails, Medication, PatientsMonthlyStatistics
from doctor.models import Doctor, DoctorNotification, DoctorSchedule, DoctorStats, Remark, UsersViewed, Medicine, MonthlyStatistics
from cebuMap.models import CebuMap, Incidence, CebuBarangays
from .models import AdminNotification



admin.site.site_header = 'Aidsecure Admininistrator Page'
admin.site.site_title = 'Aidsecure'
admin.site.index_title = 'Aidsecure Site Admin'

admin.site.unregister(Group)
admin.site.unregister(User)

class DoctorAdmin(admin.ModelAdmin):
    search_fields = ('name', 'email', 'hospital_name', 'login_flag',)
    list_display = ('name', 'email', 'hospital_name', 'login_flag',)
    list_filter = ('name', 'hospital_name', 'login_flag',)

class DoctorNotificationAdmin(admin.ModelAdmin):
    search_fields = ('name', 'action_type', 'patient_username', 'action_taken', 'notif_status',)
    list_display = ('name', 'action_type', 'patient_username', 'action_taken', 'notif_status',) 
    list_filter = ('name', 'action_type', 'patient_username', 'action_taken', 'notif_status',)

class DoctorScheduleAdmin(admin.ModelAdmin):
    search_fields = ('doc_in_charge', 'schedule_date', 'patient_username',  'status',)#'status',
    list_display = ('doc_in_charge', 'schedule_date', 'patient_username', 'status',)
    list_filter = ('doc_in_charge',  'schedule_date', 'patient_username',  'status',)

class DoctorStatsAdmin(admin.ModelAdmin):
    search_fields = ('doctor_name',)
    list_display = ('doctor_name', 'doc_patients_count',)
    list_filter = ('doctor_name',)

class DocMonthlyStatsAdmin(admin.ModelAdmin):
    search_fields = ('year', 'doctor_name',)
    list_display = ('year', 'doctor_name', 'pk',)
    list_filter = ('year', 'doctor_name',)

class MedicinesAdmin(admin.ModelAdmin):
    search_fields = ('drug_name', 'medicine_type', 'drug_group', 'availability',)
    list_display = ('drug_name', 'medicine_type', 'drug_group', 'availability',)
    list_filter = ('drug_name', 'medicine_type', 'drug_group', 'availability',)

class PatientAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'HIV_status', 'login_flag',)
    search_fields = ('username', 'email', 'HIV_status', 'login_flag', 'present_address',)
    list_filter= ('username', 'email', 'HIV_status', 'login_flag', 'present_address',)

class ICRFormAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_visit', 'purpose_of_visit',)
    search_fields = ('first_name', 'last_name', 'date_of_visit', 'purpose_of_visit',)
    list_filter = ('first_name', 'last_name', 'date_of_visit', 'purpose_of_visit',)

class MedHistFormAdmin(admin.ModelAdmin):
    list_display = ('username','date_diagnosed', 'created_on',)
    search_fields  = ('username','date_diagnosed', 'created_on',)
    list_filter  = ('username','date_diagnosed', 'created_on',)

class ProfileFormAdmin(admin.ModelAdmin):
    list_display = ('code_name', 'address',)
    search_fields = ('code_name', 'address',)
    list_filter = ('code_name', 'address',)

class PersonalRecordAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'created_on',)
    search_fields = ('author', 'title', 'created_on',)
    list_filter = ('author', 'title', 'created_on',)

class PatientNotificationAdmin(admin.ModelAdmin):
    list_display = ('patient_username', 'subject', 'action_type', 'doctor_name', 'notif_status',)
    search_fields = ('patient_username', 'subject', 'action_type', 'doctor_name', 'notif_status',)
    list_filter = ('patient_username', 'subject', 'action_type', 'doctor_name', 'notif_status',)

class PatientLocationDetailsAdmin(admin.ModelAdmin):
    list_display = ('username', 'location', 'lat', 'lon',)
    search_fields = ('username', 'location', 'lat', 'lon',)
    list_filter = ('username', 'location', 'lat', 'lon',)

class MedicationAdmin(admin.ModelAdmin):
    list_display = ('username', 'drug_name', 'medicine_type', 'administered_by',)
    search_fields = ('username', 'drug_name', 'medicine_type', 'administered_by',)
    list_filter = ('username', 'drug_name', 'medicine_type', 'administered_by',)

class RemarkAdmin(admin.ModelAdmin):
    list_display = ('author', 'remark_parent_type', 'remark_receiver', 'remark_seen',)
    list_filter = ('author', 'remark_parent_type', 'remark_receiver', 'remark_seen',)
    search_fields = ('author', 'remark_parent_type', 'remark_receiver', 'remark_seen',)

class UsersViewedAdmin(admin.ModelAdmin):
    list_display = ('viewer_name', 'viewed_type', 'file_owner', 'seen_flag',)

class CebuBarangaysAdmin(admin.ModelAdmin):
    search_fields = ('name_3',)
    list_display = ('name_3',)
    list_filter = ('name_3',)

class PatientsMonthlyStatisticsAdmin(admin.ModelAdmin):
    search_fields = ('year', 'patient_username',)
    list_display = ('year', 'patient_username',)
    list_filter = ('year', 'patient_username',)

class CebuMapAdmin(LeafletGeoAdmin):
    list_display = ['my_clickable_link']
    readonly_fields = ('my_clickable_link',)
    exclude = ['location']

    def my_clickable_link(self, instance):
        return format_html(
            '<a href="http://202.92.153.70:80/cebuMap" target="_blank">Cebu HIV Incidence Map</a>', 
        )

    my_clickable_link.short_description = "Cebu Map"

    
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(DoctorNotification, DoctorNotificationAdmin)
admin.site.register(DoctorSchedule, DoctorScheduleAdmin)
admin.site.register(DoctorStats, DoctorStatsAdmin)
admin.site.register(Remark, RemarkAdmin) # no need for the general admin to be seen
admin.site.register(Medicine, MedicinesAdmin)
admin.site.register(MonthlyStatistics, DocMonthlyStatsAdmin)

admin.site.register(Patient, PatientAdmin)
admin.site.register(ICRForm, ICRFormAdmin)
admin.site.register(ProfileForm, ProfileFormAdmin)
admin.site.register(MedHistForm, MedHistFormAdmin)
admin.site.register(PersonalRecord, PersonalRecordAdmin)
admin.site.register(UsersViewed, UsersViewedAdmin)
admin.site.register(Medication, MedicationAdmin)
admin.site.register(PatientsMonthlyStatistics, PatientsMonthlyStatisticsAdmin)

admin.site.register(PatientNotification, PatientNotificationAdmin) 

admin.site.register(PatientLocationDetails, PatientLocationDetailsAdmin)

admin.site.register(CebuMap, CebuMapAdmin)
admin.site.register(CebuBarangays, CebuBarangaysAdmin)

