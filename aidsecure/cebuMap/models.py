from __future__ import unicode_literals
from django.db import models
from django.contrib.gis.db import models as gis_models
from patient.models import Patient

class CebuMap(models.Model):
    location = gis_models.PointField(null=True)
    class Meta:
        verbose_name_plural = "Cebu Map"

class Incidence(models.Model):
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50, null=True)
    location = gis_models.PointField(null=True)
    modifiable = False
    

    def __unicode__(self):
        return self.name
    
# from ogr- manually type in shell to auto create this model
# use load.run() in python shell afterwards
class CebuBarangays(models.Model):
    objectid = models.IntegerField()

    # hiv incidence data every barangay
    hiv_pop = models.ManyToManyField(Patient, related_name="brgy_hiv_pop", blank=True)
    stage_1 = models.ManyToManyField(Patient, related_name="brgy_stage_1", blank=True)
    stage_2 = models.ManyToManyField(Patient, related_name="brgy_stage_2", blank=True)
    stage_3 = models.ManyToManyField(Patient, related_name="brgy_stage_3", blank=True)
    stage_0 = models.ManyToManyField(Patient, related_name="brgy_stage_0", blank=True) # negative, do not add in hiv pop
    for_screening =  models.ManyToManyField(Patient, related_name="brgy_screening", blank=True) # untested patient
    deceased = models.ManyToManyField(Patient, related_name="brgy_deceased", blank=True)
    migrated = models.ManyToManyField(Patient, related_name="brgy_migrated", blank=True) # way gamit

    iso = models.CharField(max_length=254, blank=True)
    name_0 = models.CharField(max_length=254, blank=True)
    name_1 = models.CharField(max_length=254, blank=True)
    varname_1 = models.CharField(max_length=254, blank=True)
    nl_name_1 = models.CharField(max_length=254, blank=True)
    hasc_1 = models.CharField(max_length=254, blank=True)
    fips_1 = models.CharField(max_length=254, blank=True)
    cc_1 = models.CharField(max_length=254, blank=True)
    type_1 = models.CharField(max_length=254, blank=True)
    engtype_1 = models.CharField(max_length=254, blank=True)
    validfr_1 = models.CharField(max_length=254, blank=True)
    validto_1 = models.CharField(max_length=254, blank=True)
    remarks_1 = models.CharField(max_length=254, blank=True)
    name_2 = models.CharField(max_length=254, blank=True)
    varname_2 = models.CharField(max_length=254, blank=True)
    nl_name_2 = models.CharField(max_length=254, blank=True)
    hasc_2 = models.CharField(max_length=254, blank=True)
    fips_2 = models.CharField(max_length=254, blank=True)
    cc_2 = models.CharField(max_length=254, blank=True)
    type_2 = models.CharField(max_length=254, blank=True)
    engtype_2 = models.CharField(max_length=254, blank=True)
    validfr_2 = models.CharField(max_length=254, blank=True)
    validto_2 = models.CharField(max_length=254, blank=True)
    remarks_2 = models.CharField(max_length=254, blank=True)
    name_3 = models.CharField(max_length=254, blank=True)   #brgy name
    varname_3 = models.CharField(max_length=254, blank=True)
    nl_name_3 = models.CharField(max_length=254, blank=True)
    hasc_3 = models.CharField(max_length=254, blank=True)
    type_3 = models.CharField(max_length=254, blank=True)
    engtype_3 = models.CharField(max_length=254, blank=True)
    validfr_3 = models.CharField(max_length=254, blank=True)
    validto_3 = models.CharField(max_length=254, blank=True)
    remarks_3 = models.CharField(max_length=254, blank=True)
    name_4 = models.CharField(max_length=254, blank=True)
    varname_4 = models.CharField(max_length=254, blank=True)
    type_4 = models.CharField(max_length=254, blank=True)
    engtype_4 = models.CharField(max_length=254, blank=True)
    validfr_4 = models.CharField(max_length=254, blank=True)
    validto_4 = models.CharField(max_length=254, blank=True)
    remarks_4 = models.CharField(max_length=254, blank=True)
    name_5 = models.CharField(max_length=254, blank=True)
    type_5 = models.CharField(max_length=254, blank=True)
    engtype_5 = models.CharField(max_length=254, blank=True)
    validfr_5 = models.CharField(max_length=254, blank=True)
    validto_5 = models.CharField(max_length=254, blank=True)
    shape_leng = models.FloatField( blank=True)
    shape_area = models.FloatField( blank=True)
    bngy = models.CharField(max_length=30, blank=True)
    psgc_bgy = models.CharField(max_length=15, blank=True)
    geom = gis_models.MultiPolygonField(srid=4326, blank=True)




    def __str__(self):
        return self.name_3

    class Meta:
        verbose_name_plural = "Cebu Barangays"
