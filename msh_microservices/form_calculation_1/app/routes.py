from flask import Flask, request, jsonify
from app import app
import json



data_compare = {
    "labour_population": False,
    "labour_constant_population": False,
    "labour_labour": False,
    "labour_government_workers": False,
    "labour_private_labour":False,
    "labour_private_ogorod": False,
    "labour_total_econ_inactive_population":False,
    "labour_unemployed":False,
    "labour_household_size":False,
    "labour_average_income_family": False,
    "house_total_dvor": False,
    "house_zaselen_dvor": False,
    "dh_count":False,
    "dx_number_ogorodov":False,
    "dx_cx_land": False,
    "dx_pashnya": False,
    "dx_mnogoletnie": False,
    "dx_zelej": False,
    "dx_pastbishe": False,
    "dx_senokosy": False,
    "dx_ogorody": False,
    "dx_sad": False,
    "dx_urojai": False,
    "dx_cucumber": False,
    "dx_tomato": False,
    "dx_potato": False,
    "dx_kapusta": False,
    "dx_carrot": False,
    "dx_svekla": False,
    "dx_sweet_peper": False,
    "dx_baklajan": False,
    "dx_kabachek": False,
    "dx_onion": False,
    "dx_chesnok": False,
    "dx_redis": False,
    "dx_korm": False,
    "dx_fruits": False,
    "kx_amount": False,
    "kz_cx_land": False,
    "kx_pansya": False,
    "kx_mnogoletnie": False,
    "kx_zelej": False,
    "kx_pastbishe": False,
    "kx_senokosy": False,
    "kx_urojai": False,
    "kx_zerno": False,
    "kx_rice": False,
    "kx_maslichnye": False,
    "kx_korm": False,
    "kx_mnogoletnie_derevo": False,
    "kz_cx_land_reserve": False,
    "kx_pansya_reserve": False,
    "kx_mnogoletnie_reserve": False,
    "kx_zelej_reserve": False,
    "kx_pastbishe_reserve": False,
    "kx_senokosy_reserve": False,
    "infrastructure_polivochnaya_sistema_":False,
    "infrastructure_polivochnaya_sistema_isused":False,
    "infrastructure_polivy": False,
    "infrastructure_mtm":False,
    "infrastructure_mtm_isused":False,
    "infrastructure_slad":False,
    "infrastructure_slad_isused":False,
    "infrastructure_garage":False,
    "infrastructure_garage_isused":False,
    "infrastructure_cycsterny":False,
    "infrastructure_cycsterny_isused":False,
    "infrastructure_transformator":False,
    "infrastructure_transformator_isused":False,
    "specialization_rastenivodstvo_value": False,
    "animal_dvor": False,
    "animal_skot_bird": False,
    "animal_cx_land": False,
    "animal_pashnya": False,
    "animal_mnogolet": False,
    "animal_zalej": False,
    "animal_pastbisha": False,
    "animal_senokos": False,
    "animal_ogorod": False,
    "animal_sad": False,
    "animal_krs_milk": False,
    "animal_krs_meat":False,
    "animal_sheep": False,
    "animal_kozel": False,
    "animal_horse": False,
    "animal_camel":False,
    "animal_pig":False,
    "animal_chicken": False,
    "animal_gusi":False,
    "animal_duck":False,
    "animal_induk":False,
    "animal_mik_total": False,
    "animal_milk_cow": False,
    "animal_milkrate_cow": False,
    "animal_mil_kozel": False,
    "animal_milrate_kozel": False,
    "animal_milk_horse": False,
    "animal_milkrate_horse": False,
    "animal_milk_camel": False,
    "animal_milkrate_camel": False,
    "animal_meat_total": False,
    "animal_meat_cow": False,
    "animal_meat_sheep": False,
    "animal_meat_horse": False,
    "animal_meat_pig": False,
    "animal_meat_camel": False,
    "animal_meat_chicken": False,
    "animal_meat_duck": False,
    "animal_meat_gusi": False,
    "animal_egg_total": False,
    "animal_egg_chicken": False,
    "animal_egg_gusi":False,
    "animal_egg_perepel":False,
    "animal_transformator":False,
    "animal_transformator_isused":False,
    "specialization_animal_value": False,
    "noncx_sto":False,
    "noncx_sto_needs":False,
    "noncx_kindergarden":False,
    "noncx_kindergarden_needs":False,
    "noncx_souvenier":False,
    "noncx_souvenier_needs":False,
    "noncx_pc_service":False,
    "noncx_pc_service_needs":False,
    "noncx_store":False,
    "noncx_store_needs":False,
    "noncx_remont_bytovoi_tech":False,
    "noncx_remont_bytovoi_tech_needs":False,
    "noncx_metal":False,
    "noncx_metal_needs":False,
    "noncx_accounting":False,
    "noncx_accounting_needs":False,
    "noncx_photo":False,
    "noncx_photo_needs":False,
    "noncx_turism":False,
    "noncx_turism_needs":False,
    "noncx_rent":False,
    "noncx_rent_needs":False,
    "noncx_cargo":False,
    "noncx_cargo_needs":False,
    "noncx_massage":False,
    "noncx_massage_needs":False,
    "noncx_foodcourt":False,
    "noncx_foodcourt_needs":False,
    "noncx_cleaning":False,
    "noncx_cleaning_needs":False,
    "noncx_beuty":False,
    "noncx_beuty_needs":False,
    "noncx_carwash":False,
    "noncx_carwash_needs":False,
    "noncx_atelie":False,
    "noncx_atelie_needs":False,
    "noncx_others":False,
    "noncx_others_needs":False,
    "noncx_stroika":False,
    "noncx_stroika_needs":False,
    "noncx_mebel":False,
    "noncx_mebel_needs":False,
    "noncx_stroi_material":False,
    "noncx_stroi_material_needs":False,
    "noncx_svarka":False,
    "noncx_svarka_needs":False,
    "noncx_woodworking":False,
    "noncx_woodworking_needs":False,
    "noncx_others_uslugi":False,
    "noncx_others_needs_uslugi":False,
    "manufacture_milk": False,
    "manufacture_milk_needs": False,
    "manufacture_meat": False,
    "manufacture_meat_needs": False,
    "manufacture_vegetables": False,
    "manufacture_vegetables_needs": False,
    "manufacture_mayo": False,
    "manufacture_mayo_needs": False,
    "manufacture_fish": False,
    "manufacture_fish_needs": False,
    "manufacture_choco": False,
    "manufacture_choco_needs": False,
    "manufacture_beer": False,
    "manufacture_beer_needs": False,
    "manufacture_vodka": False,
    "manufacture_vodka_needs": False,
    "manufacture_honey": False,
    "manufacture_honey_needs": False,
    "manufacture_polufabricat": False,
    "manufacture_polufabricat_needs": False,
    "manufacture_bread": False,
    "manufacture_bread_needs": False,
    "manufacture_others": False,
    "manufacture_others_needs": False,
    "credit_amount": False,
    "credit_total": False,
    "credit_average_total":False,
    "credit_zalog": False,
}

def get_key(data:dict):
    for key in data:
        yield key


@app.route('/form_calc_1',  methods=['POST'])
def form_calc_1():
    data: dict = request.get_json()
    
    formdata = json.loads(data.get('formdata'))
    formdata_go = json.loads(data.get('formdata_go'))
    if not formdata_go:
        return jsonify(data_compare)
    for key in get_key(data_compare):
        if ((0<=formdata_go[key])
            and (formdata_go[key] * 1.2 < formdata[key] 
            or (formdata_go[key]) * 0.8 > formdata[key])):
            data_compare[key] = True

    return jsonify(data_compare)
    
        