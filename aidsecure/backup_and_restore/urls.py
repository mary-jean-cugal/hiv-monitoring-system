from django.conf.urls import include, url
from . import  views
from django.urls import path

urlpatterns=[
    url(r'^backup-data/$',  views.backupAidsecure, name='backUp'),
    url(r'^restore-data/$',  views.restoreAidsecure, name='restore'),
]

