#import os
import os, sys
sys.path.insert(0, os.path.abspath(".."))

from django.contrib.gis.utils import LayerMapping
from cebuMap.models import CebuMap, CebuBarangays

# open python shell, from cebuMap import load_layer, load_layer.run()
# Auto-generated `LayerMapping` dictionary for CebuBarangays model
cebubarangays_mapping = {
    'objectid': 'OBJECTID',
    'iso': 'ISO',
    'name_0': 'NAME_0',
    'name_1': 'NAME_1',
    'varname_1': 'VARNAME_1',
    'nl_name_1': 'NL_NAME_1',
    'hasc_1': 'HASC_1',
    'fips_1': 'FIPS_1',
    'cc_1': 'CC_1',
    'type_1': 'TYPE_1',
    'engtype_1': 'ENGTYPE_1',
    'validfr_1': 'VALIDFR_1',
    'validto_1': 'VALIDTO_1',
    'remarks_1': 'REMARKS_1',
    'name_2': 'NAME_2',
    'varname_2': 'VARNAME_2',
    'nl_name_2': 'NL_NAME_2',
    'hasc_2': 'HASC_2',
    'fips_2': 'FIPS_2',
    'cc_2': 'CC_2',
    'type_2': 'TYPE_2',
    'engtype_2': 'ENGTYPE_2',
    'validfr_2': 'VALIDFR_2',
    'validto_2': 'VALIDTO_2',
    'remarks_2': 'REMARKS_2',
    'name_3': 'NAME_3',
    'varname_3': 'VARNAME_3',
    'nl_name_3': 'NL_NAME_3',
    'hasc_3': 'HASC_3',
    'type_3': 'TYPE_3',
    'engtype_3': 'ENGTYPE_3',
    'validfr_3': 'VALIDFR_3',
    'validto_3': 'VALIDTO_3',
    'remarks_3': 'REMARKS_3',
    'name_4': 'NAME_4',
    'varname_4': 'VARNAME_4',
    'type_4': 'TYPE_4',
    'engtype_4': 'ENGTYPE_4',
    'validfr_4': 'VALIDFR_4',
    'validto_4': 'VALIDTO_4',
    'remarks_4': 'REMARKS_4',
    'name_5': 'NAME_5',
    'type_5': 'TYPE_5',
    'engtype_5': 'ENGTYPE_5',
    'validfr_5': 'VALIDFR_5',
    'validto_5': 'VALIDTO_5',
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'bngy': 'bngy',
    'psgc_bgy': 'psgc_bgy',
    'geom': 'MULTIPOLYGON',
}

# Auto-generated `LayerMapping` dictionary for cebuMap model
# from ogrchuchu manually type in shell to auto create this model
cebumap_mapping = {
    'objectid': 'OBJECTID',
    'iso': 'ISO',
    'name_0': 'NAME_0',
    'name_1': 'NAME_1',
    'varname_1': 'VARNAME_1',
    'nl_name_1': 'NL_NAME_1',
    'hasc_1': 'HASC_1',
    'fips_1': 'FIPS_1',
    'cc_1': 'CC_1',
    'type_1': 'TYPE_1',
    'engtype_1': 'ENGTYPE_1',
    'validfr_1': 'VALIDFR_1',
    'validto_1': 'VALIDTO_1',
    'remarks_1': 'REMARKS_1',
    'name_2': 'NAME_2',
    'varname_2': 'VARNAME_2',
    'nl_name_2': 'NL_NAME_2',
    'hasc_2': 'HASC_2',
    'fips_2': 'FIPS_2',
    'cc_2': 'CC_2',
    'type_2': 'TYPE_2',
    'engtype_2': 'ENGTYPE_2',
    'validfr_2': 'VALIDFR_2',
    'validto_2': 'VALIDTO_2',
    'remarks_2': 'REMARKS_2',
    'name_3': 'NAME_3',
    'varname_3': 'VARNAME_3',
    'nl_name_3': 'NL_NAME_3',
    'hasc_3': 'HASC_3',
    'type_3': 'TYPE_3',
    'engtype_3': 'ENGTYPE_3',
    'validfr_3': 'VALIDFR_3',
    'validto_3': 'VALIDTO_3',
    'remarks_3': 'REMARKS_3',
    'name_4': 'NAME_4',
    'varname_4': 'VARNAME_4',
    'type_4': 'TYPE_4',
    'engtype_4': 'ENGTYPE_4',
    'validfr_4': 'VALIDFR_4',
    'validto_4': 'VALIDTO_4',
    'remarks_4': 'REMARKS_4',
    'name_5': 'NAME_5',
    'type_5': 'TYPE_5',
    'engtype_5': 'ENGTYPE_5',
    'validfr_5': 'VALIDFR_5',
    'validto_5': 'VALIDTO_5',
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'bngy': 'bngy',
    'psgc_bgy': 'psgc_bgy',
    'geom': 'MULTIPOLYGON',
}


cebu_shp = os.path .abspath(os.path.join(os.path.dirname(__file__), 'cebu_data/cebu_cebu.shp'))


def run(verbose=True):
    lm = LayerMapping(CebuBarangays, cebu_shp, cebubarangays_mapping, transform=False,encoding='iso-8859-1' )
    lm.save(strict=True, verbose=verbose)
