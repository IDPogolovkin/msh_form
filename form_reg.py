from app import app, bcrypt, db
from app.models import *
import csv


app.app_context().push()

# csv_file_path = 'form_aul_amanat.csv'
# counter = 0
# with open(csv_file_path, 'r', encoding='utf-8') as file:
#     csv_reader = csv.reader(file)

#     next(csv_reader)
#     for row in csv_reader:
        
#         user = User.query.filter_by(kato_6=row[6],).first()
#         form = Form(
#             user_id = user.id,
#             kato_2 = row[2],
#             kato_2_name = row[3],
#             kato_4 = row[4],
#             kato_4_name = row[5],
#             kato_6 = row[6],
#             kato_6_name = row[7],
#             form_year = row[8],
#             labour_population = row[9],
#             labour_constant_population = row[10],
#             labour_labour = row[11],
#             labour_government_workers = row[12],
#             labour_private_labour = row[13],
#             labour_private_ogorod = row[14],
#             labour_total_econ_inactive_population = row[15],
#             labour_unemployed = row[16],
#             labour_household_size = row[17],
#             labour_average_income_family = row[18],
#             house_total_dvor = row[19],
#             house_zaselen_dvor = row[20],
#             dh_count = row[21],
#             dx_number_ogorodov = row[22],
#             dx_cx_land = row[23],
#             dx_pashnya = row[24],
#             dx_mnogoletnie = row[25],
#             dx_zelej = row[26],
#             dx_pastbishe = row[27],
#             dx_senokosy = row[28],
#             dx_ogorody = row[29],
#             dx_sad = row[30],
#             dx_urojai = row[31],
#             dx_cucumber = row[32],
#             dx_tomato = row[33],
#             dx_potato = row[34],
#             dx_kapusta = row[35],
#             dx_carrot = row[36],
#             dx_svekla = row[37],
#             dx_sweet_peper = row[38],
#             dx_baklajan = row[39],
#             dx_kabachek = row[40],
#             dx_onion = row[41],
#             dx_chesnok = row[42],
#             dx_redis = row[43],
#             dx_korm = row[44],
#             dx_fruits = row[45],
#             kx_amount = row[46],
#             kz_cx_land = row[47],
#             kx_pansya = row[48],
#             kx_mnogoletnie = row[49],
#             kx_zelej = row[50],
#             kx_pastbishe = row[51],
#             kx_senokosy = row[52],
#             kx_urojai = row[53],
#             kx_zerno = row[54],
#             kx_rice = row[55],
#             kx_maslichnye = row[56],
#             kx_korm = row[57],
#             kx_mnogoletnie_derevo = row[58],
#             kz_cx_land_reserve = row[59],
#             kx_pansya_reserve = row[60],
#             kx_mnogoletnie_reserve = row[61],
#             kx_zelej_reserve = row[62],
#             kx_pastbishe_reserve = row[63],
#             kx_senokosy_reserve = row[64],
#             infrastructure_polivochnaya_sistema_ = row[65],
#             infrastructure_polivochnaya_sistema_isused = row[66],
#             infrastructure_polivy = row[67],
#             infrastructure_mtm = row[68],
#             infrastructure_mtm_isused = row[69],
#             infrastructure_slad = row[70],
#             infrastructure_slad_isused = row[71],
#             infrastructure_garage = row[72],
#             infrastructure_garage_isused = row[73],
#             infrastructure_cycsterny = row[74],
#             infrastructure_cycsterny_isused = row[75],
#             infrastructure_transformator = row[76],
#             infrastructure_transformator_isused = row[77],
#             specialization_rastenivodstvo = row[78],
#             animal_dvor = row[79],
#             animal_skot_bird = row[80],
#             animal_cx_land = row[81],
#             animal_pashnya = row[82],
#             animal_mnogolet = row[83],
#             animal_zalej = row[84],
#             animal_pastbisha = row[85],
#             animal_senokos = row[86],
#             animal_ogorod = row[87],
#             animal_sad = row[88],
#             animal_krs_milk = row[89],
#             animal_krs_meat = row[90],
#             animal_sheep = row[91],
#             animal_kozel = row[92],
#             animal_horse = row[93],
#             animal_camel = row[94],
#             animal_pig = row[95],
#             animal_chicken = row[96],
#             animal_gusi = row[97],
#             animal_duck = row[98],
#             animal_induk = row[99],
#             animal_mik_total = row[100],
#             animal_milk_cow = row[101],
#             animal_milkrate_cow = row[102],
#             animal_mil_kozel = row[103],
#             animal_milrate_kozel = row[104],
#             animal_milk_horse = row[105],
#             animal_milkrate_horse = row[106],
#             animal_milk_camel = row[107],
#             animal_milkrate_camel = row[108],
#             animal_meat_total = row[109],
#             animal_meat_cow = row[110],
#             animal_meat_sheep = row[111],
#             animal_meat_horse = row[112],
#             animal_meat_pig = row[113],
#             animal_meat_camel = row[114],
#             animal_meat_chicken = row[115],
#             animal_meat_duck = row[116],
#             animal_meat_gusi = row[117],
#             animal_egg_total = row[118],
#             animal_egg_chicken = row[119],
#             animal_egg_gusi = row[120],
#             animal_egg_perepel = row[121],
#             animal_transformator = row[122],
#             animal_transformator_isused = row[123],
#             specialization_animal = row[124],
#             noncx_sto = row[125],
#             noncx_sto_needs = row[126],
#             noncx_kindergarden = row[127],
#             noncx_kindergarden_needs = row[128],
#             noncx_souvenier = row[129],
#             noncx_souvenier_needs = row[130],
#             noncx_pc_service = row[131],
#             noncx_pc_service_needs = row[132],
#             noncx_store = row[133],
#             noncx_store_needs = row[134],
#             noncx_remont_bytovoi_tech = row[135],
#             noncx_remont_bytovoi_tech_needs = row[136],
#             noncx_metal = row[137],
#             noncx_metal_needs = row[138],
#             noncx_accounting = row[139],
#             noncx_accounting_needs = row[140],
#             noncx_photo = row[141],
#             noncx_photo_needs = row[142],
#             noncx_turism = row[143],
#             noncx_turism_needs = row[144],
#             noncx_rent = row[145],
#             noncx_rent_needs = row[146],
#             noncx_cargo = row[147],
#             noncx_cargo_needs = row[148],
#             noncx_massage = row[149],
#             noncx_massage_needs = row[150],
#             noncx_foodcourt = row[151],
#             noncx_foodcourt_needs = row[152],
#             noncx_cleaning = row[153],
#             noncx_cleaning_needs = row[154],
#             noncx_beuty = row[155],
#             noncx_beuty_needs = row[156],
#             noncx_carwash = row[157],
#             noncx_carwash_needs = row[158],
#             noncx_atelie = row[159],
#             noncx_atelie_needs = row[160],
#             noncx_others = row[161],
#             noncx_others_needs = row[162],
#             noncx_stroika = row[163],
#             noncx_stroika_needs = row[164],
#             noncx_mebel = row[165],
#             noncx_mebel_needs = row[166],
#             noncx_stroi_material = row[167],
#             noncx_stroi_material_needs = row[168],
#             noncx_svarka = row[169],
#             noncx_svarka_needs = row[170],
#             noncx_woodworking = row[171],
#             noncx_woodworking_needs = row[172],
#             noncx_others_uslugi = row[173],
#             noncx_others_needs_uslugi = row[174],
#             manufacture_milk = row[175],
#             manufacture_milk_needs = row[176],
#             manufacture_meat = row[177],
#             manufacture_meat_needs = row[178],
#             manufacture_vegetables = row[179],
#             manufacture_vegetables_needs = row[180],
#             manufacture_mayo = row[181],
#             manufacture_mayo_needs = row[182],
#             manufacture_fish = row[183],
#             manufacture_fish_needs = row[184],
#             manufacture_choco = row[185],
#             manufacture_choco_needs = row[186],
#             manufacture_beer = row[187],
#             manufacture_beer_needs = row[188],
#             manufacture_vodka = row[189],
#             manufacture_vodka_needs = row[190],
#             manufacture_honey = row[191],
#             manufacture_honey_needs = row[192],
#             manufacture_polufabricat = row[193],
#             manufacture_polufabricat_needs = row[194],
#             manufacture_bread = row[195],
#             manufacture_bread_needs = row[196],
#             manufacture_others = row[197],
#             manufacture_others_needs = row[198],
#             credit_amount = row[199],
#             credit_total = row[200],
#             credit_average_total = row[201],
#             credit_zalog = row[202],

#         )
                
#         db.session.add(form)
#         db.session.commit()
#         counter += 1
#         print(counter, '-', form)


csv_file_path = 'sdu_form.csv'
counter = 0
with open(csv_file_path, 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)

    next(csv_reader)
    
    for row in csv_reader:
        
        form = Form_G_O(
            kato_2 = row[0],
            kato_2_name = row[1],
            kato_4 = row[2],
            kato_4_name = row[3],
            kato_6 = row[4],
            kato_6_name = row[5],
            form_year = row[6],
            labour_population = row[7],
            labour_constant_population = row[8],
            labour_labour = row[9],
            labour_government_workers = row[10],
            labour_private_labour = row[11],
            labour_private_ogorod = row[12],
            labour_total_econ_inactive_population = row[13],
            labour_unemployed = row[14],
            labour_household_size = row[15],
            labour_average_income_family = row[16],
            house_total_dvor = row[17],
            house_zaselen_dvor = row[18],
            dh_count = row[19],
            dx_number_ogorodov = row[20],
            dx_cx_land = row[21],
            dx_pashnya = row[22],
            dx_mnogoletnie = row[23],
            dx_zelej = row[24],
            dx_pastbishe = row[25],
            dx_senokosy = row[26],
            dx_ogorody = row[27],
            dx_sad = row[28],
            dx_urojai = row[29],
            dx_cucumber = row[30],
            dx_tomato = row[31],
            dx_potato = row[32],
            dx_kapusta = row[33],
            dx_carrot = row[34],
            dx_svekla = row[35],
            dx_sweet_peper = row[36],
            dx_baklajan = row[37],
            dx_kabachek = row[38],
            dx_onion = row[39],
            dx_chesnok = row[40],
            dx_redis = row[41],
            dx_korm = row[42],
            dx_fruits = row[43],
            kx_amount = row[44],
            kz_cx_land = row[45],
            kx_pansya = row[46],
            kx_mnogoletnie = row[47],
            kx_zelej = row[48],
            kx_pastbishe = row[49],
            kx_senokosy = row[50],
            kx_urojai = row[51],
            kx_zerno = row[52],
            kx_rice = row[53],
            kx_maslichnye = row[54],
            kx_korm = row[55],
            kx_mnogoletnie_derevo = row[56],
            kz_cx_land_reserve = row[57],
            kx_pansya_reserve = row[58],
            kx_mnogoletnie_reserve = row[59],
            kx_zelej_reserve = row[60],
            kx_pastbishe_reserve = row[61],
            kx_senokosy_reserve = row[62],
            infrastructure_polivochnaya_sistema_ = row[63],
            infrastructure_polivochnaya_sistema_isused = row[64],
            infrastructure_polivy = row[65],
            infrastructure_mtm = row[66],
            infrastructure_mtm_isused = row[67],
            infrastructure_slad = row[68],
            infrastructure_slad_isused = row[69],
            infrastructure_garage = row[70],
            infrastructure_garage_isused = row[71],
            infrastructure_cycsterny = row[72],
            infrastructure_cycsterny_isused = row[73],
            infrastructure_transformator = row[74],
            infrastructure_transformator_isused = row[75],
            specialization_rastenivodstvo = row[76],
            animal_dvor = row[77],
            animal_skot_bird = row[78],
            animal_cx_land = row[79],
            animal_pashnya = row[80],
            animal_mnogolet = row[81],
            animal_zalej = row[82],
            animal_pastbisha = row[83],
            animal_senokos = row[84],
            animal_ogorod = row[85],
            animal_sad = row[86],
            animal_krs_milk = row[87],
            animal_krs_meat = row[88],
            animal_sheep = row[89],
            animal_kozel = row[90],
            animal_horse = row[91],
            animal_camel = row[92],
            animal_pig = row[93],
            animal_chicken = row[94],
            animal_gusi = row[95],
            animal_duck = row[96],
            animal_induk = row[97],
            animal_mik_total = row[98],
            animal_milk_cow = row[99],
            animal_milkrate_cow = row[100],
            animal_mil_kozel = row[101],
            animal_milrate_kozel = row[102],
            animal_milk_horse = row[103],
            animal_milkrate_horse = row[104],
            animal_milk_camel = row[105],
            animal_milkrate_camel = row[106],
            animal_meat_total = row[107],
            animal_meat_cow = row[108],
            animal_meat_sheep = row[109],
            animal_meat_horse = row[110],
            animal_meat_pig = row[111],
            animal_meat_camel = row[112],
            animal_meat_chicken = row[113],
            animal_meat_duck = row[114],
            animal_meat_gusi = row[115],
            animal_egg_total = row[116],
            animal_egg_chicken = row[117],
            animal_egg_gusi = row[118],
            animal_egg_perepel = row[119],
            animal_transformator = row[120],
            animal_transformator_isused = row[121],
            specialization_animal = row[122],
            noncx_sto = row[123],
            noncx_sto_needs = row[124],
            noncx_kindergarden = row[125],
            noncx_kindergarden_needs = row[126],
            noncx_souvenier = row[127],
            noncx_souvenier_needs = row[128],
            noncx_pc_service = row[129],
            noncx_pc_service_needs = row[130],
            noncx_store = row[131],
            noncx_store_needs = row[132],
            noncx_remont_bytovoi_tech = row[133],
            noncx_remont_bytovoi_tech_needs = row[134],
            noncx_metal = row[135],
            noncx_metal_needs = row[136],
            noncx_accounting = row[137],
            noncx_accounting_needs = row[138],
            noncx_photo = row[139],
            noncx_photo_needs = row[140],
            noncx_turism = row[141],
            noncx_turism_needs = row[142],
            noncx_rent = row[143],
            noncx_rent_needs = row[144],
            noncx_cargo = row[145],
            noncx_cargo_needs = row[146],
            noncx_massage = row[147],
            noncx_massage_needs = row[148],
            noncx_foodcourt = row[149],
            noncx_foodcourt_needs = row[150],
            noncx_cleaning = row[151],
            noncx_cleaning_needs = row[152],
            noncx_beuty = row[153],
            noncx_beuty_needs = row[154],
            noncx_carwash = row[155],
            noncx_carwash_needs = row[156],
            noncx_atelie = row[157],
            noncx_atelie_needs = row[158],
            noncx_others = row[159],
            noncx_others_needs = row[160],
            noncx_stroika = row[161],
            noncx_stroika_needs = row[162],
            noncx_mebel = row[163],
            noncx_mebel_needs = row[164],
            noncx_stroi_material = row[165],
            noncx_stroi_material_needs = row[166],
            noncx_svarka = row[167],
            noncx_svarka_needs = row[168],
            noncx_woodworking = row[169],
            noncx_woodworking_needs = row[170],
            noncx_others_uslugi = row[171],
            noncx_others_needs_uslugi = row[172],
            manufacture_milk = row[173],
            manufacture_milk_needs = row[174],
            manufacture_meat = row[175],
            manufacture_meat_needs = row[176],
            manufacture_vegetables = row[177],
            manufacture_vegetables_needs = row[178],
            manufacture_mayo = row[179],
            manufacture_mayo_needs = row[180],
            manufacture_fish = row[181],
            manufacture_fish_needs = row[182],
            manufacture_choco = row[183],
            manufacture_choco_needs = row[184],
            manufacture_beer = row[185],
            manufacture_beer_needs = row[186],
            manufacture_vodka = row[187],
            manufacture_vodka_needs = row[188],
            manufacture_honey = row[189],
            manufacture_honey_needs = row[190],
            manufacture_polufabricat = row[191],
            manufacture_polufabricat_needs = row[192],
            manufacture_bread = row[193],
            manufacture_bread_needs = row[194],
            manufacture_others = row[195],
            manufacture_others_needs = row[196],
            credit_amount = row[197],
            credit_total = row[198],
            credit_average_total = row[199],
            credit_zalog = row[200],
        )
        db.session.add(form)
        db.session.commit()
