from django.urls import path
from . import views
from portal import views as portalViews
from django.conf.urls import include, url



urlpatterns = [
    url(r'^patientLogout/$', views.patientLogout, name = 'patientLogout'),
    url(r'^icrForm/$', views.editICR, name = 'editICR'),
    url(r'^addDoctor/$', views.addDr, name='addDocs'),
    url(r'^removeDoctor/$', views.removeDr, name='removeDocs'),
    url(r'^addNewRecord/$', views.createNewPersonalRecord, name='newPRecord'),
    url(r'^addpendingSched/$', views.addPendingSched, name='addPSched'),
    url(r'^seenRemark/$', views.seenRemark, name="seenRemark"),
    url(r'^editAcc/$', views.editAccInfo, name="editAcc"),
    url(r'^patientNotifRead/$', views.notifRead, name='patientNotifRead'),
    url(r'^patientChangeProfPic/$', views.changeProfPic, name='patientChangeProfPic'),
]

