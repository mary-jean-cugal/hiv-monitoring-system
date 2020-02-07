from django.views.generic import View
from django.utils import timezone

from django.shortcuts import render
from .render import Render

from django.views.generic import TemplateView
from django.core.serializers import serialize
from django.http import HttpResponse
from .models import CebuBarangays
from patient.models import PatientLocationDetails, Patient

def bngy_datasets(request):
    brgys = CebuBarangays.objects.all()
    counties = serialize('geojson', brgys) 
    return HttpResponse(counties, content_type='json')

def default_map(request):
    patient_loc = PatientLocationDetails.objects.all()
    all_brgys = CebuBarangays.objects.order_by('name_3')
    outside_cebu = Patient.objects.filter(status="outside cebu")
    context={
        'all_brgys': all_brgys,
        'patient_loc': patient_loc,
        'outside_ceb': outside_cebu,

    }
    
    return render(request, 'cebuMap\cebu_hiv_map.html', context)

def get_data(request):
    download_brgys = request.GET.getlist('checked_brgys[]')
    brgys_data = []
    print("barangays data: ", len(download_brgys))
    for brgy in download_brgys:
        brgys_data.append(CebuBarangays.objects.all().get(name_3=brgy))
    
    print("obj len: ", brgys_data)
    return brgys_data



