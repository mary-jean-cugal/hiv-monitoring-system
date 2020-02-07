from django.urls import path
from . import views
from portal import views as portalViews

from django.conf.urls import include, url

urlpatterns = [
    url(r'^docLogOut/$', views.docLogout, name = 'docLogout'),
    url(r'^editmedhist/$', views.docEditMedHist, name = 'docMedhist'),
    url(r'^addcomment/$', views.addComment, name = 'addcomment'),
    url(r'^acceptsched/$', views.acceptSched, name = 'acceptSched'),
    url(r'^rejectsched/$', views.rejectSched, name = 'rejectSched'),
    url(r'^schedfinished/$', views.finishSched, name = 'schedFinished'),
    url(r'^doceditICR/$', views.docEditICR, name = 'docEditICR'),
    url(r'^addRemark/$', views.addARemark, name = 'addRemark'),
    url(r'^addSeen/$', views.addSeenDoc, name='addSeen'),
    url(r'^addMeds/$', views.addMeds, name='addMeds'),
    url(r'^updatePStat/$', views.docUpdatePStat, name='updatePStat'),
    url(r'^docNotifRead/$', views.notifRead, name='docNotifRead'),
    url(r'^docChangeProfPic/$', views.changeProfPic, name='docChangeProfPic'),

]