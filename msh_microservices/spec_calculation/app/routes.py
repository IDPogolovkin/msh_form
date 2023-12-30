from flask import Flask, request, jsonify
from app import app
import json
from statistics import mean


def spec_calc(form, additional_info):
    result = {
        "spec_rast": 0.0,
        "spec_animal": 0.0
    }

    credit_amount_average_all = additional_info['credit_amount_average_all']
    credit_total_all = additional_info['credit_total_all']
    credit_average_total_all = additional_info['credit_average_total_all'] / additional_info['forms_len']

    w_min = min(form['dx_tomato'], form['dx_potato'], form['dx_cucumber'], form['dx_carrot'], form['dx_kapusta'], form['dx_svekla'], form['dx_onion'], form['dx_sweet_peper'], form['dx_chesnok'], form['dx_kabachek'], form['dx_fruits'], form['dx_korm'], form['dx_baklajan'], form['dx_redis'])
    w_max = max(form['dx_tomato'], form['dx_potato'], form['dx_cucumber'], form['dx_carrot'], form['dx_kapusta'], form['dx_svekla'], form['dx_onion'], form['dx_sweet_peper'], form['dx_chesnok'], form['dx_kabachek'], form['dx_fruits'], form['dx_korm'], form['dx_baklajan'], form['dx_redis'])

    f1w1 = ((float((form['dx_tomato'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w2 = ((float((form['dx_cucumber'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w3 = ((float((form['dx_potato'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w4 = ((float((form['dx_carrot'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w5 = ((float((form['dx_kapusta'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w6 = ((float((form['dx_svekla'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w7 = ((float((form['dx_onion'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w8 = ((float((form['dx_sweet_peper'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w9 = ((float((form['dx_chesnok'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w10 = ((float((form['dx_kabachek'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w11 = ((float((form['dx_fruits'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w12 = ((float((form['dx_korm'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w13 = ((float((form['dx_baklajan'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w14 = ((float((form['dx_redis'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    variables = [f1w1, f1w2, f1w3, f1w4, f1w5, f1w6, f1w7, f1w8, f1w9, f1w10, f1w11, f1w12, f1w13, f1w14]
    #non_zero_values = [value for value in variables if value != 0]
    f1_average = mean(variables) #if non_zero_values else 0
    
    f2_w_min = min(form['dx_pashnya'], form['dx_mnogoletnie'], form['dx_zelej'], form['dx_pastbishe'], form['dx_senokosy'], form['dx_ogorody'], form['dx_sad'])
    f2_w_max = max(form['dx_pashnya'], form['dx_mnogoletnie'], form['dx_zelej'], form['dx_pastbishe'], form['dx_senokosy'], form['dx_ogorody'], form['dx_sad'])
    f2w1 = ((float((form['dx_pashnya'] - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w2 = ((float((form['dx_mnogoletnie'] - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w3 = ((float((form['dx_zelej'] - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w4 = ((float((form['dx_pastbishe'] - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w5 = ((float((form['dx_senokosy'] - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w6 = ((float((form['dx_ogorody'] - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w7 = ((float((form['dx_sad'] - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    variables = [f2w1, f2w2, f2w3, f2w4, f2w5, f2w6, f2w7]
    #non_zero_values = [value for value in variables if value != 0]
    f2_average = mean(variables) #if non_zero_values else 0
    

    f3_w_min = min(form['labour_private_ogorod'], form['labour_unemployed'], form['labour_total_econ_inactive_population'], form['labour_labour'], form['labour_government_workers'], form['labour_private_labour'])
    f3_w_max = max(form['labour_private_ogorod'], form['labour_unemployed'], form['labour_total_econ_inactive_population'], form['labour_labour'], form['labour_government_workers'], form['labour_private_labour'])
    f3w1 = ((float((form['labour_private_ogorod'] - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.2 if f3_w_max - f3_w_min > 0 else 0
    f3w2 = ((float((form['labour_unemployed'] - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.2 if f3_w_max - f3_w_min > 0 else 0
    f3w3 = ((float((form['labour_total_econ_inactive_population'] - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.2 if f3_w_max - f3_w_min > 0 else 0
    f3w4 = ((float((form['labour_labour'] - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.2 if f3_w_max - f3_w_min > 0 else 0
    f3w5 = ((float((form['labour_government_workers'] - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.2 if f3_w_max - f3_w_min > 0 else 0
    f3w6 = ((float((form['labour_private_labour'] - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.2 if f3_w_max - f3_w_min > 0 else 0
    variables = [f3w1, f3w2, f3w3, f3w4, f3w5, f3w6]
    #non_zero_values = [value for value in variables if value != 0]
    f3_average = mean(variables) #if non_zero_values else 0
    
    f4w1 = form['infrastructure_mtm'] * 0.2
    f4w2 = form['infrastructure_slad'] * 0.2
    f4w3 = form['infrastructure_garage'] * 0.2
    f4w4 = form['infrastructure_cycsterny'] * 0.2
    f4w5 = form['infrastructure_transformator'] * 0.2
    f4w6 = form['infrastructure_polivochnaya_sistema_'] * 0.2
    variables = [f4w1, f4w2, f4w3, f4w4, f4w5, f4w6]
    #non_zero_values = [value for value in variables if value != 0]
    f4_average = mean(variables) #if non_zero_values else 0

    f6w1 = float((form['labour_average_income_family'] / 120000) * 0.15)
    f6w2 = float((form['credit_amount'] / credit_amount_average_all) * 0.15) if credit_amount_average_all > 0 else 0
    f6w3 = float((form['credit_total'] / credit_total_all) * 0.15) if credit_total_all > 0 else 0
    f6w4 = float((form['credit_average_total'] / credit_average_total_all) * 0.15) if credit_average_total_all > 0 else 0
    f6w5 = float(form['credit_zalog'])
    variables = [f6w1, f6w2, f6w3, f6w4, f6w5]
    #non_zero_values = [value for value in variables if value != 0]
    f6_average = mean(variables) #if non_zero_values else 0
    
    factors_total_plant = round(f1_average + f2_average + f3_average + f4_average + f6_average, 1)
    result['spec_rast'] = factors_total_plant


    #animal
    credit_amount_average_all = additional_info['credit_amount_average_all']
    credit_total_all = additional_info['credit_total_all']
    credit_average_total_all = additional_info['credit_average_total_all'] / additional_info['forms_len']

    w_min = min(form['animal_krs_milk'], form['animal_krs_meat'], form['animal_sheep'], form['animal_kozel'], form['animal_horse'], form['animal_chicken'], form['animal_gusi'], form['animal_duck'], form['animal_induk'], form['animal_camel'], form['animal_pig'])
    w_max = max(form['animal_krs_milk'], form['animal_krs_meat'], form['animal_sheep'], form['animal_kozel'], form['animal_horse'], form['animal_chicken'], form['animal_gusi'], form['animal_duck'], form['animal_induk'], form['animal_camel'], form['animal_pig'])
    f1w1 = ((float((form['animal_krs_milk'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w2 = ((float((form['animal_krs_meat'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w3 = ((float((form['animal_sheep'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w4 = ((float((form['animal_kozel'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w5 = ((float((form['animal_horse'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w6 = ((float((form['animal_chicken'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w7 = ((float((form['animal_gusi'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w8 = ((float((form['animal_duck'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w9 = ((float((form['animal_induk'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w10 = ((float((form['animal_camel'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w11 = ((float((form['animal_pig'] - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    variables = [f1w1, f1w2, f1w3, f1w4, f1w5, f1w6, f1w7, f1w8, f1w9, f1w10, f1w11]
    # #non_zero_values = [value for value in variables if value != 0]
    f1_average = mean(variables) #if non_zero_values else 0

    f2_w_min = min(form['animal_meat_cow'], form['animal_meat_sheep'], form['animal_meat_horse'], form['animal_meat_chicken'], form['animal_milk_cow'], form['animal_mil_kozel'], form['animal_milk_horse'], form['animal_egg_chicken'], form['animal_meat_pig'], form['animal_meat_camel'], form['animal_meat_duck'], form['animal_meat_gusi'], form['animal_egg_perepel'], form['animal_milk_camel'])
    f2_w_max = max(form['animal_meat_cow'], form['animal_meat_sheep'], form['animal_meat_horse'], form['animal_meat_chicken'], form['animal_milk_cow'], form['animal_mil_kozel'], form['animal_milk_horse'], form['animal_egg_chicken'], form['animal_meat_pig'], form['animal_meat_camel'], form['animal_meat_duck'], form['animal_meat_gusi'], form['animal_egg_perepel'], form['animal_milk_camel'])
    f2w1 = ((float((form['animal_meat_cow'] - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w2 = ((float((form['animal_meat_sheep'] - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w3 = ((float((form['animal_meat_horse'] - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w4 = ((float((form['animal_meat_chicken'] - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w5 = ((float((form['animal_milk_cow'] - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w6 = ((float((form['animal_mil_kozel'] - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w7 = ((float((form['animal_milk_horse'] - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w8 = ((float((form['animal_egg_chicken'] - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w9 = ((float((form['animal_meat_pig'] - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w10 = ((float((form['animal_meat_camel'] - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w11 = ((float((form['animal_meat_duck'] - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w12 = ((float((form['animal_meat_gusi'] - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w13 = ((float((form['animal_egg_gusi'] - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w14 = ((float((form['animal_egg_perepel'] - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w15 = ((float((form['animal_milk_camel'] - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    variables = [f2w1, f2w2, f2w3, f2w4, f2w5, f2w6, f2w7, f2w8, f2w9, f2w10, f2w11, f2w12, f2w13, f2w14, f2w15]
    #non_zero_values = [value for value in variables if value != 0]
    f2_average = mean(variables) #if non_zero_values else 0

    f3_w_min = min(form['animal_pashnya'], form['animal_mnogolet'], form['animal_zalej'], form['animal_pastbisha'], form['animal_senokos'], form['animal_ogorod'], form['animal_sad'])
    f3_w_max = max(form['animal_pashnya'], form['animal_mnogolet'], form['animal_zalej'], form['animal_pastbisha'], form['animal_senokos'], form['animal_ogorod'], form['animal_sad'])
    f3w1 = ((float((form['animal_pashnya'] - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.1 if f3_w_max - f3_w_min > 0 else 0
    f3w2 = ((float((form['animal_mnogolet'] - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.1 if f3_w_max - f3_w_min > 0 else 0
    f3w3 = ((float((form['animal_zalej'] - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.1 if f3_w_max - f3_w_min > 0 else 0
    f3w4 = ((float((form['animal_pastbisha'] - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.1 if f3_w_max - f3_w_min > 0 else 0
    f3w5 = ((float((form['animal_senokos'] - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.1 if f3_w_max - f3_w_min > 0 else 0
    f3w6 = ((float((form['animal_ogorod'] - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.1 if f3_w_max - f3_w_min > 0 else 0
    f3w7 = ((float((form['animal_sad'] - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.1 if f3_w_max - f3_w_min > 0 else 0
    variables = [f3w1, f3w2, f3w3, f3w4, f3w5, f3w6, f3w7]
    #non_zero_values = [value for value in variables if value != 0]
    f3_average = mean(variables) #if non_zero_values else 0

    f4_w_min = min(form['labour_private_ogorod'], form['labour_unemployed'], form['labour_total_econ_inactive_population'], form['labour_labour'], form['labour_government_workers'], form['labour_private_labour'])
    f4_w_max = max(form['labour_private_ogorod'], form['labour_unemployed'], form['labour_total_econ_inactive_population'], form['labour_labour'], form['labour_government_workers'], form['labour_private_labour'])
    f4w1 = ((float((form['labour_private_ogorod'] - f4_w_min) / (f4_w_max - f4_w_min))) * 100) * 0.2 if f4_w_max - f4_w_min > 0 else 0
    f4w2 = ((float((form['labour_unemployed'] - f4_w_min) / (f4_w_max - f4_w_min))) * 100) * 0.2 if f4_w_max - f4_w_min > 0 else 0
    f4w3 = ((float((form['labour_total_econ_inactive_population'] - f4_w_min) / (f4_w_max - f4_w_min))) * 100) * 0.2 if f4_w_max - f4_w_min > 0 else 0
    f4w4 = ((float((form['labour_labour'] - f4_w_min) / (f4_w_max - f4_w_min))) * 100) * 0.2 if f4_w_max - f4_w_min > 0 else 0
    f4w5 = ((float((form['labour_government_workers'] - f4_w_min) / (f4_w_max - f4_w_min))) * 100) * 0.2 if f4_w_max - f4_w_min > 0 else 0
    f4w6 = ((float((form['labour_private_labour'] - f4_w_min) / (f4_w_max - f4_w_min))) * 100) * 0.2 if f4_w_max - f4_w_min > 0 else 0
    variables = [f4w1, f4w2, f4w3, f4w4, f4w5, f4w6]
    #non_zero_values = [value for value in variables if value != 0]
    f4_average = mean(variables) #if non_zero_values else 0

    f5w1 = form['infrastructure_mtm'] * 0.15
    f5w2 = form['infrastructure_slad'] * 0.15
    f5w3 = form['infrastructure_garage'] * 0.15
    f5w4 = form['infrastructure_cycsterny'] * 0.15
    f5w5 = form['infrastructure_transformator'] * 0.15
    f5w6 = form['infrastructure_polivochnaya_sistema_'] * 0.15
    variables = [f5w1, f5w2, f5w3, f5w4, f5w5, f5w6]
    #non_zero_values = [value for value in variables if value != 0]
    f5_average = mean(variables) #if non_zero_values else 0
    
    f7w1 = float((form['labour_average_income_family'] / 120000)) * 0.15 
    f7w2 = float((form['credit_amount'] / credit_amount_average_all) * 0.15) if credit_amount_average_all > 0 else 0
    f7w3 = float((form['credit_total'] / credit_total_all) * 0.15) if credit_total_all > 0 else 0
    f7w4 = float((form['credit_average_total'] / credit_average_total_all) * 0.15) if credit_average_total_all > 0 else 0
    f7w5 = float(form['credit_zalog'])
    variables = [f7w1, f7w2, f7w3, f7w4, f7w5]
    #non_zero_values = [value for value in variables if value != 0]
    f7_average = mean(variables) #if non_zero_values else 0
    factors_total_animal = round(f1_average + f2_average + f3_average + f4_average + f5_average + f7_average, 1)
    result['spec_animal'] =factors_total_animal


        
    return result


@app.route('/spec_calc',  methods=['POST'])
def form_calc_1():
    data: dict = request.get_json()

    formdata = json.loads(data.get('formdata'))
    additional_info = json.loads(data.get('additional_info'))
    spec_calc(formdata, additional_info)
    return jsonify(spec_calc(formdata, additional_info))
    
        