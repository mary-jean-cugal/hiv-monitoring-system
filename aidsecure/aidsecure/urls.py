
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# from django.views.static import serve

urlpatterns = [
    url(r'^aidsecure-admin/', admin.site.urls),
    url(r'^', include('portal.urls')),
    url(r'^',  include('patient.urls')),
    url(r'^',  include('doctor.urls')),
    url(r'^', include('cebuMap.urls')),
] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)