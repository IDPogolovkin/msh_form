from app import app, bcrypt, db
from app.models import *
import csv
from sqlalchemy.inspection import inspect


app.app_context().push()

# spec_calculation = Spec_calculation

forms = Form.query.all()
counter = 0
for form in forms:
    formRegion = Form.query.filter_by(kato_4 = form.kato_4).all()
    inspector1 = inspect(Form)
    columns = inspector1.columns.keys()
    sum_formdata = Form(
        **{column: sum(getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in formRegion)
            for column in columns}
    )

    credit_amount_average_all = sum_formdata.credit_amount
    credit_average_total_all = sum_formdata.credit_average_total
    credit_total_all = sum_formdata.credit_total
    credit_average_total_all = sum_formdata.credit_average_total / len(formRegion)

    w_min = min(formData.animal_krs_milk, formData.animal_krs_meat, formData.animal_sheep, formData.animal_kozel, formData.animal_horse, formData.animal_chicken, formData.animal_gusi, formData.animal_duck, formData.animal_induk)
    w_max = max(formData.animal_krs_milk, formData.animal_krs_meat, formData.animal_sheep, formData.animal_kozel, formData.animal_horse, formData.animal_chicken, formData.animal_gusi, formData.animal_duck, formData.animal_induk)
    f1w1 = ((float((formData.animal_krs_milk - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w2 = ((float((formData.animal_krs_meat - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w3 = ((float((formData.animal_sheep - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w4 = ((float((formData.animal_kozel - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w5 = ((float((formData.animal_horse - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w6 = ((float((formData.animal_chicken - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w7 = ((float((formData.animal_gusi - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w8 = ((float((formData.animal_duck - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w9 = ((float((formData.animal_induk - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1_average = statistics.mean([f1w1, f1w2, f1w3, f1w4, f1w5, f1w6, f1w7, f1w8, f1w9])

    eggs_tonn = (formData.animal_egg_chicken * 60) / 1000000
    f2_w_min = min(formData.animal_meat_cow, formData.animal_meat_sheep, formData.animal_meat_horse, formData.animal_meat_chicken, formData.animal_milk_cow, formData.animal_mil_kozel, formData.animal_milk_horse, Decimal(eggs_tonn))
    f2_w_max = max(formData.animal_meat_cow, formData.animal_meat_sheep, formData.animal_meat_horse, formData.animal_meat_chicken, formData.animal_milk_cow, formData.animal_mil_kozel, formData.animal_milk_horse, Decimal(eggs_tonn))
    f2w1 = ((float((formData.animal_meat_cow - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w2 = ((float((formData.animal_meat_sheep - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w3 = ((float((formData.animal_meat_horse - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w4 = ((float((formData.animal_meat_chicken - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w5 = ((float((formData.animal_milk_cow - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w6 = ((float((formData.animal_mil_kozel - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w7 = ((float((formData.animal_milk_horse - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w8 = ((float((Decimal(eggs_tonn) - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2_average = statistics.mean([f2w1, f2w2, f2w3, f2w4, f2w5, f2w6, f2w7, f2w8])

    f3_w_min = min(formData.animal_pashnya, formData.animal_mnogolet, formData.animal_zalej, formData.animal_pastbisha, formData.animal_senokos, formData.animal_ogorod, formData.animal_sad)
    f3_w_max = max(formData.animal_pashnya, formData.animal_mnogolet, formData.animal_zalej, formData.animal_pastbisha, formData.animal_senokos, formData.animal_ogorod, formData.animal_sad)
    f3w1 = ((float((formData.animal_pashnya - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.1 if f3_w_max - f3_w_min > 0 else 0
    f3w2 = ((float((formData.animal_mnogolet - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.1 if f3_w_max - f3_w_min > 0 else 0
    f3w3 = ((float((formData.animal_zalej - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.1 if f3_w_max - f3_w_min > 0 else 0
    f3w4 = ((float((formData.animal_pastbisha - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.1 if f3_w_max - f3_w_min > 0 else 0
    f3w5 = ((float((formData.animal_senokos - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.1 if f3_w_max - f3_w_min > 0 else 0
    f3w6 = ((float((formData.animal_ogorod - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.1 if f3_w_max - f3_w_min > 0 else 0
    f3w7 = ((float((formData.animal_sad - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.1 if f3_w_max - f3_w_min > 0 else 0
    f3_average = statistics.mean([f3w1, f3w2, f3w3, f3w4, f3w5, f3w6, f3w7])

    f4_w_min = min(formData.labour_private_ogorod, formData.labour_unemployed, formData.labour_total_econ_inactive_population)
    f4_w_max = max(formData.labour_private_ogorod, formData.labour_unemployed, formData.labour_total_econ_inactive_population)
    f4w1 = ((float((formData.labour_private_ogorod - f4_w_min) / (f4_w_max - f4_w_min))) * 100) * 0.2 if f4_w_max - f4_w_min > 0 else 0
    f4w2 = ((float((formData.labour_unemployed - f4_w_min) / (f4_w_max - f4_w_min))) * 100) * 0.2 if f4_w_max - f4_w_min > 0 else 0
    f4w3 = ((float((formData.labour_total_econ_inactive_population - f4_w_min) / (f4_w_max - f4_w_min))) * 100) * 0.2 if f4_w_max - f4_w_min > 0 else 0
    f4_average = statistics.mean([f4w1, f4w2, f4w3])

    f5w1 = formData.infrastructure_mtm * 0.15
    f5w2 = formData.infrastructure_slad * 0.15
    f5w3 = formData.infrastructure_garage * 0.15
    f5w4 = formData.infrastructure_cycsterny * 0.15
    f5w5 = formData.infrastructure_transformator * 0.15
    f5w6 = formData.infrastructure_polivochnaya_sistema_ * 0.15
    f5_average = statistics.mean([f5w1, f5w2, f5w3, f5w4, f5w5, f5w6])
    
    f7w1 = float((formData.labour_average_income_family / 120000)) * 0.15 
    f7w2 = float(formData.credit_amount / (credit_average_total_all / credit_amount_average_all)) * 0.15 if credit_amount_average_all > 0 else 0
    f7w3 = float(formData.credit_total / credit_total_all) * 0.15 if credit_total_all > 0 else 0
    f7w4 = float(formData.credit_average_total / credit_average_total_all) * 0.15 if credit_average_total_all > 0 else 0
    f7w5 = float(formData.credit_zalog)
    f7_average = statistics.mean([f7w1, f7w2, f7w3, f7w4, f7w5])
    factors_total = round(f1_average + f2_average + f3_average + f4_average + f5_average + f7_average, 2)
