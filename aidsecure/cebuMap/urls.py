from django.conf.urls import include, url
from . import  views
from django.urls import path

urlpatterns=[
    url(r'^cebuMap/$', views.default_map, name='cebuMap'),
    url(r'^bngy_data/$',  views.bngy_datasets, name='bngy'),
       
]
