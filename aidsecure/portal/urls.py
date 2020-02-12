from django.urls import path
from . import views
from patient import views as patientViews
from doctor import views as doctorViews
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.setPortal, name = 'portalDefault'),
    path('aidsecure/', views.setPortal, name = 'portal'),
    path('patient-profile/<slug>/', views.validatePatient, name='patientLogin'),
    path('doc-profile/<slug>/', views.validateDoctor, name='docLogin'),
    path('aidsecure/patient-sign-up', views.addPatient, name = 'signUpPatient'),
    path('aidsecure/doctor-sign-up', views.addDoctor, name = 'signUpDoctor'),
    
]
