from app import app, db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from datetime import timedelta, datetime, timezone

# class User_district(db.Model, UserMixin):
#    id = db.Column(db.Integer, primary_key = True)
#    login = db.Column(db.String(250))
#    kato_2 = db.Column(db.String(1024))
#    kato_2_name = db.Column(db.String(1024))
#    kato_4 = db.Column(db.String(1024))
#    kato_4_name = db.Column(db.String(1024))
#    password = db.Column(db.String(250))
#    is_district = db.Column(db.Boolean)
#    def __repr__(self):
#       return f"KATO_2('{self.kato_2}'), KATO_4('{self.kato_4}')"


class User(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key = True)
   login = db.Column(db.String(250), unique=True)
   kato_2 = db.Column(db.String(1024))
   kato_2_name = db.Column(db.String(1024))
   kato_4 = db.Column(db.String(1024))
   kato_4_name = db.Column(db.String(1024))
   kato_6 = db.Column(db.String(1024), unique=True)
   kato_6_name = db.Column(db.String(1024))
   password = db.Column(db.String(250))
   is_district = db.Column(db.Boolean)
   is_obl = db.Column(db.Boolean)
   def __repr__(self):
      return f"KATO_2('{self.kato_2}'), KATO_4('{self.kato_4}'),  KATO_6('{self.kato_6}')"

class Form(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   user = relationship("User",backref="forms")
   kato_2 = db.Column(db.String(1024))
   kato_2_name = db.Column(db.String(1024))
   kato_4 = db.Column(db.String(1024))
   kato_4_name = db.Column(db.String(1024))
   kato_6 = db.Column(db.String(1024))
   kato_6_name = db.Column(db.String(1024))
   form_year = db.Column(db.String(1024))
   labour_population = db.Column(db.BigInteger)
   labour_constant_population = db.Column(db.BigInteger)
   labour_labour = db.Column(db.BigInteger)
   labour_government_workers = db.Column(db.BigInteger)
   labour_private_labour = db.Column(db.BigInteger)
   labour_private_ogorod = db.Column(db.BigInteger)
   labour_total_econ_inactive_population = db.Column(db.BigInteger)
   labour_unemployed = db.Column(db.BigInteger)
   labour_household_size = db.Column(db.BigInteger)
   labour_average_income_family = db.Column(db.BigInteger)
   house_total_dvor = db.Column(db.BigInteger)
   house_zaselen_dvor = db.Column(db.BigInteger)
   dh_count = db.Column(db.BigInteger)
   dx_number_ogorodov = db.Column(db.BigInteger)
   dx_cx_land = db.Column(db.Numeric(30, 1))
   dx_pashnya = db.Column(db.Numeric(30, 1))
   dx_mnogoletnie = db.Column(db.Numeric(30, 1))
   dx_zelej = db.Column(db.Numeric(30, 1))
   dx_pastbishe = db.Column(db.Numeric(30, 1))
   dx_senokosy = db.Column(db.Numeric(30, 1))
   dx_ogorody = db.Column(db.Numeric(30, 1))
   dx_sad = db.Column(db.Numeric(30, 1))
   dx_urojai = db.Column(db.Numeric(30, 1))
   dx_cucumber = db.Column(db.Numeric(30, 1))
   dx_tomato = db.Column(db.Numeric(30, 1))
   dx_potato = db.Column(db.Numeric(30, 1))
   dx_kapusta = db.Column(db.Numeric(30, 1))
   dx_carrot = db.Column(db.Numeric(30, 1))
   dx_svekla = db.Column(db.Numeric(30, 1))
   dx_sweet_peper = db.Column(db.Numeric(30, 1))
   dx_baklajan = db.Column(db.Numeric(30, 1))
   dx_kabachek = db.Column(db.Numeric(30, 1))
   dx_onion = db.Column(db.Numeric(30, 1))
   dx_chesnok = db.Column(db.Numeric(30, 1))
   dx_redis = db.Column(db.Numeric(30, 1))
   dx_korm = db.Column(db.Numeric(30, 1))
   dx_fruits = db.Column(db.Numeric(30, 1))
   kx_amount = db.Column(db.BigInteger)
   kz_cx_land = db.Column(db.Numeric(30, 1))
   kx_pansya = db.Column(db.Numeric(30, 1))
   kx_mnogoletnie = db.Column(db.Numeric(30, 1))
   kx_zelej = db.Column(db.Numeric(30, 1))
   kx_pastbishe = db.Column(db.Numeric(30, 1))
   kx_senokosy = db.Column(db.Numeric(30, 1))
   kx_urojai = db.Column(db.Numeric(30, 1))
   kx_zerno = db.Column(db.Numeric(30, 1))
   kx_rice = db.Column(db.Numeric(30, 1))
   kx_maslichnye = db.Column(db.Numeric(30, 1))
   kx_korm = db.Column(db.Numeric(30, 1))
   kx_mnogoletnie_derevo = db.Column(db.Numeric(30, 1))
   kz_cx_land_reserve = db.Column(db.Numeric(30, 1))
   kx_pansya_reserve = db.Column(db.Numeric(30, 1))
   kx_mnogoletnie_reserve = db.Column(db.Numeric(30, 1))
   kx_zelej_reserve = db.Column(db.Numeric(30, 1))
   kx_pastbishe_reserve = db.Column(db.Numeric(30, 1))
   kx_senokosy_reserve = db.Column(db.Numeric(30, 1))
   infrastructure_polivochnaya_sistema_ = db.Column(db.BigInteger)
   infrastructure_polivochnaya_sistema_isused = db.Column(db.BigInteger)
   infrastructure_polivy = db.Column(db.Numeric(30, 1))
   infrastructure_mtm = db.Column(db.BigInteger)
   infrastructure_mtm_isused = db.Column(db.BigInteger)
   infrastructure_slad = db.Column(db.BigInteger)
   infrastructure_slad_isused = db.Column(db.BigInteger)
   infrastructure_garage = db.Column(db.BigInteger)
   infrastructure_garage_isused = db.Column(db.BigInteger)
   infrastructure_cycsterny = db.Column(db.BigInteger)
   infrastructure_cycsterny_isused = db.Column(db.BigInteger)
   infrastructure_transformator = db.Column(db.BigInteger)
   infrastructure_transformator_isused = db.Column(db.BigInteger)
   specialization_rastenivodstvo = db.Column(db.String(1024))
   specialization_rastenivodstvo_value = db.Column(db.Numeric(30, 1))
   animal_dvor = db.Column(db.BigInteger)
   animal_skot_bird = db.Column(db.BigInteger)
   animal_cx_land = db.Column(db.Numeric(30, 1))
   animal_pashnya = db.Column(db.Numeric(30, 1))
   animal_mnogolet = db.Column(db.Numeric(30, 1))
   animal_zalej = db.Column(db.Numeric(30, 1))
   animal_pastbisha = db.Column(db.Numeric(30, 1))
   animal_senokos = db.Column(db.Numeric(30, 1))
   animal_ogorod = db.Column(db.Numeric(30, 1))
   animal_sad = db.Column(db.Numeric(30, 1))
   animal_krs_milk = db.Column(db.BigInteger)
   animal_krs_meat = db.Column(db.BigInteger)
   animal_sheep = db.Column(db.BigInteger)
   animal_kozel = db.Column(db.BigInteger)
   animal_horse = db.Column(db.BigInteger)
   animal_camel = db.Column(db.BigInteger)
   animal_pig = db.Column(db.BigInteger)
   animal_chicken = db.Column(db.BigInteger)
   animal_gusi = db.Column(db.BigInteger)
   animal_duck = db.Column(db.BigInteger)
   animal_induk = db.Column(db.BigInteger)
   animal_mik_total = db.Column(db.Numeric(30, 1))
   animal_milk_cow = db.Column(db.Numeric(30, 1))
   animal_milkrate_cow = db.Column(db.Numeric(30, 1))
   animal_mil_kozel = db.Column(db.Numeric(30, 1))
   animal_milrate_kozel = db.Column(db.Numeric(30, 1))
   animal_milk_horse = db.Column(db.Numeric(30, 1))
   animal_milkrate_horse = db.Column(db.Numeric(30, 1))
   animal_milk_camel = db.Column(db.Numeric(30, 1))
   animal_milkrate_camel = db.Column(db.Numeric(30, 1))
   animal_meat_total = db.Column(db.Numeric(30, 1))
   animal_meat_cow = db.Column(db.Numeric(30, 1))
   animal_meat_sheep = db.Column(db.Numeric(30, 1))
   animal_meat_horse = db.Column(db.Numeric(30, 1))
   animal_meat_pig = db.Column(db.Numeric(30, 1))
   animal_meat_camel = db.Column(db.Numeric(30, 1))
   animal_meat_chicken = db.Column(db.Numeric(30, 1))
   animal_meat_duck = db.Column(db.Numeric(30, 1))
   animal_meat_gusi = db.Column(db.Numeric(30, 1))
   animal_egg_total = db.Column(db.BigInteger)
   animal_egg_chicken = db.Column(db.BigInteger)
   animal_egg_gusi = db.Column(db.BigInteger)
   animal_egg_perepel = db.Column(db.BigInteger)
   animal_transformator = db.Column(db.BigInteger)
   animal_transformator_isused = db.Column(db.BigInteger)
   specialization_animal = db.Column(db.String(1024))
   specialization_animal_value = db.Column(db.Numeric(30, 1))
   noncx_sto = db.Column(db.BigInteger)
   noncx_sto_needs = db.Column(db.BigInteger)
   noncx_kindergarden = db.Column(db.BigInteger)
   noncx_kindergarden_needs = db.Column(db.BigInteger)
   noncx_souvenier = db.Column(db.BigInteger)
   noncx_souvenier_needs = db.Column(db.BigInteger)
   noncx_pc_service = db.Column(db.BigInteger)
   noncx_pc_service_needs = db.Column(db.BigInteger)
   noncx_store = db.Column(db.BigInteger)
   noncx_store_needs = db.Column(db.BigInteger)
   noncx_remont_bytovoi_tech = db.Column(db.BigInteger)
   noncx_remont_bytovoi_tech_needs = db.Column(db.BigInteger)
   noncx_metal = db.Column(db.BigInteger)
   noncx_metal_needs = db.Column(db.BigInteger)
   noncx_accounting = db.Column(db.BigInteger)
   noncx_accounting_needs = db.Column(db.BigInteger)
   noncx_photo = db.Column(db.BigInteger)
   noncx_photo_needs = db.Column(db.BigInteger)
   noncx_turism = db.Column(db.BigInteger)
   noncx_turism_needs = db.Column(db.BigInteger)
   noncx_rent = db.Column(db.BigInteger)
   noncx_rent_needs = db.Column(db.BigInteger)
   noncx_cargo = db.Column(db.BigInteger)
   noncx_cargo_needs = db.Column(db.BigInteger)
   noncx_massage = db.Column(db.BigInteger)
   noncx_massage_needs = db.Column(db.BigInteger)
   noncx_foodcourt = db.Column(db.BigInteger)
   noncx_foodcourt_needs = db.Column(db.BigInteger)
   noncx_cleaning = db.Column(db.BigInteger)
   noncx_cleaning_needs = db.Column(db.BigInteger)
   noncx_beuty = db.Column(db.BigInteger)
   noncx_beuty_needs = db.Column(db.BigInteger)
   noncx_carwash = db.Column(db.BigInteger)
   noncx_carwash_needs = db.Column(db.BigInteger)
   noncx_atelie = db.Column(db.BigInteger)
   noncx_atelie_needs = db.Column(db.BigInteger)
   noncx_others = db.Column(db.BigInteger)
   noncx_others_needs = db.Column(db.BigInteger)
   noncx_stroika = db.Column(db.BigInteger)
   noncx_stroika_needs = db.Column(db.BigInteger)
   noncx_mebel = db.Column(db.BigInteger)
   noncx_mebel_needs = db.Column(db.BigInteger)
   noncx_stroi_material = db.Column(db.BigInteger)
   noncx_stroi_material_needs = db.Column(db.BigInteger)
   noncx_svarka = db.Column(db.BigInteger)
   noncx_svarka_needs = db.Column(db.BigInteger)
   noncx_woodworking = db.Column(db.BigInteger)
   noncx_woodworking_needs = db.Column(db.BigInteger)
   noncx_others_uslugi = db.Column(db.BigInteger)
   noncx_others_needs_uslugi = db.Column(db.BigInteger)
   manufacture_milk = db.Column(db.Numeric(30, 1))
   manufacture_milk_needs = db.Column(db.Numeric(30, 1))
   manufacture_meat = db.Column(db.Numeric(30, 1))
   manufacture_meat_needs = db.Column(db.Numeric(30, 1))
   manufacture_vegetables = db.Column(db.Numeric(30, 1))  # Corrected typo
   manufacture_vegetables_needs = db.Column(db.Numeric(30, 1))  # Corrected typo
   manufacture_mayo = db.Column(db.Numeric(30, 1))
   manufacture_mayo_needs = db.Column(db.Numeric(30, 1))
   manufacture_fish = db.Column(db.Numeric(30, 1))
   manufacture_fish_needs = db.Column(db.Numeric(30, 1))
   manufacture_choco = db.Column(db.Numeric(30, 1))
   manufacture_choco_needs = db.Column(db.Numeric(30, 1))
   manufacture_beer = db.Column(db.Numeric(30, 1))
   manufacture_beer_needs = db.Column(db.Numeric(30, 1))
   manufacture_vodka = db.Column(db.Numeric(30, 1))
   manufacture_vodka_needs = db.Column(db.Numeric(30, 1))
   manufacture_honey = db.Column(db.Numeric(30, 1))
   manufacture_honey_needs = db.Column(db.Numeric(30, 1))
   manufacture_polufabricat = db.Column(db.Numeric(30, 1))
   manufacture_polufabricat_needs = db.Column(db.Numeric(30, 1))
   manufacture_bread = db.Column(db.Numeric(30, 1))
   manufacture_bread_needs = db.Column(db.Numeric(30, 1))
   manufacture_others = db.Column(db.Numeric(30, 1))
   manufacture_others_needs = db.Column(db.Numeric(30, 1))
   credit_amount = db.Column(db.BigInteger)
   credit_total = db.Column(db.BigInteger)
   credit_average_total = db.Column(db.BigInteger)
   credit_zalog = db.Column(db.Numeric(30, 1))
   modified_date = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone(timedelta(hours=6))), onupdate=datetime.now(timezone(timedelta(hours=6))))
   creation_date = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone(timedelta(hours=6))))

class Form_old(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   kato_2 = db.Column(db.String(1024))
   kato_2_name = db.Column(db.String(1024))
   kato_4 = db.Column(db.String(1024))
   kato_4_name = db.Column(db.String(1024))
   kato_6 = db.Column(db.String(1024))
   kato_6_name = db.Column(db.String(1024))
   form_year = db.Column(db.String(1024))
   labour_population = db.Column(db.BigInteger)
   labour_constant_population = db.Column(db.BigInteger)
   labour_labour = db.Column(db.BigInteger)
   labour_government_workers = db.Column(db.BigInteger)
   labour_private_labour = db.Column(db.BigInteger)
   labour_private_ogorod = db.Column(db.BigInteger)
   labour_total_econ_inactive_population = db.Column(db.BigInteger)
   labour_unemployed = db.Column(db.BigInteger)
   labour_household_size = db.Column(db.BigInteger)
   labour_average_income_family = db.Column(db.BigInteger)
   house_total_dvor = db.Column(db.BigInteger)
   house_zaselen_dvor = db.Column(db.BigInteger)
   dh_count = db.Column(db.BigInteger)
   dx_number_ogorodov = db.Column(db.BigInteger)
   dx_cx_land = db.Column(db.Numeric(30, 1))
   dx_pashnya = db.Column(db.Numeric(30, 1))
   dx_mnogoletnie = db.Column(db.Numeric(30, 1))
   dx_zelej = db.Column(db.Numeric(30, 1))
   dx_pastbishe = db.Column(db.Numeric(30, 1))
   dx_senokosy = db.Column(db.Numeric(30, 1))
   dx_ogorody = db.Column(db.Numeric(30, 1))
   dx_sad = db.Column(db.Numeric(30, 1))
   dx_urojai = db.Column(db.Numeric(30, 1))
   dx_cucumber = db.Column(db.Numeric(30, 1))
   dx_tomato = db.Column(db.Numeric(30, 1))
   dx_potato = db.Column(db.Numeric(30, 1))
   dx_kapusta = db.Column(db.Numeric(30, 1))
   dx_carrot = db.Column(db.Numeric(30, 1))
   dx_svekla = db.Column(db.Numeric(30, 1))
   dx_sweet_peper = db.Column(db.Numeric(30, 1))
   dx_baklajan = db.Column(db.Numeric(30, 1))
   dx_kabachek = db.Column(db.Numeric(30, 1))
   dx_onion = db.Column(db.Numeric(30, 1))
   dx_chesnok = db.Column(db.Numeric(30, 1))
   dx_redis = db.Column(db.Numeric(30, 1))
   dx_korm = db.Column(db.Numeric(30, 1))
   dx_fruits = db.Column(db.Numeric(30, 1))
   kx_amount = db.Column(db.BigInteger)
   kz_cx_land = db.Column(db.Numeric(30, 1))
   kx_pansya = db.Column(db.Numeric(30, 1))
   kx_mnogoletnie = db.Column(db.Numeric(30, 1))
   kx_zelej = db.Column(db.Numeric(30, 1))
   kx_pastbishe = db.Column(db.Numeric(30, 1))
   kx_senokosy = db.Column(db.Numeric(30, 1))
   kx_urojai = db.Column(db.Numeric(30, 1))
   kx_zerno = db.Column(db.Numeric(30, 1))
   kx_rice = db.Column(db.Numeric(30, 1))
   kx_maslichnye = db.Column(db.Numeric(30, 1))
   kx_korm = db.Column(db.Numeric(30, 1))
   kx_mnogoletnie_derevo = db.Column(db.Numeric(30, 1))
   kz_cx_land_reserve = db.Column(db.Numeric(30, 1))
   kx_pansya_reserve = db.Column(db.Numeric(30, 1))
   kx_mnogoletnie_reserve = db.Column(db.Numeric(30, 1))
   kx_zelej_reserve = db.Column(db.Numeric(30, 1))
   kx_pastbishe_reserve = db.Column(db.Numeric(30, 1))
   kx_senokosy_reserve = db.Column(db.Numeric(30, 1))
   infrastructure_polivochnaya_sistema_ = db.Column(db.BigInteger)
   infrastructure_polivochnaya_sistema_isused = db.Column(db.BigInteger)
   infrastructure_polivy = db.Column(db.Numeric(30, 1))
   infrastructure_mtm = db.Column(db.BigInteger)
   infrastructure_mtm_isused = db.Column(db.BigInteger)
   infrastructure_slad = db.Column(db.BigInteger)
   infrastructure_slad_isused = db.Column(db.BigInteger)
   infrastructure_garage = db.Column(db.BigInteger)
   infrastructure_garage_isused = db.Column(db.BigInteger)
   infrastructure_cycsterny = db.Column(db.BigInteger)
   infrastructure_cycsterny_isused = db.Column(db.BigInteger)
   infrastructure_transformator = db.Column(db.BigInteger)
   infrastructure_transformator_isused = db.Column(db.BigInteger)
   specialization_rastenivodstvo = db.Column(db.String(1024))
   specialization_rastenivodstvo_value = db.Column(db.Numeric(30, 1))
   animal_dvor = db.Column(db.BigInteger)
   animal_skot_bird = db.Column(db.BigInteger)
   animal_cx_land = db.Column(db.Numeric(30, 1))
   animal_pashnya = db.Column(db.Numeric(30, 1))
   animal_mnogolet = db.Column(db.Numeric(30, 1))
   animal_zalej = db.Column(db.Numeric(30, 1))
   animal_pastbisha = db.Column(db.Numeric(30, 1))
   animal_senokos = db.Column(db.Numeric(30, 1))
   animal_ogorod = db.Column(db.Numeric(30, 1))
   animal_sad = db.Column(db.Numeric(30, 1))
   animal_krs_milk = db.Column(db.BigInteger)
   animal_krs_meat = db.Column(db.BigInteger)
   animal_sheep = db.Column(db.BigInteger)
   animal_kozel = db.Column(db.BigInteger)
   animal_horse = db.Column(db.BigInteger)
   animal_camel = db.Column(db.BigInteger)
   animal_pig = db.Column(db.BigInteger)
   animal_chicken = db.Column(db.BigInteger)
   animal_gusi = db.Column(db.BigInteger)
   animal_duck = db.Column(db.BigInteger)
   animal_induk = db.Column(db.BigInteger)
   animal_mik_total = db.Column(db.Numeric(30, 1))
   animal_milk_cow = db.Column(db.Numeric(30, 1))
   animal_milkrate_cow = db.Column(db.Numeric(30, 1))
   animal_mil_kozel = db.Column(db.Numeric(30, 1))
   animal_milrate_kozel = db.Column(db.Numeric(30, 1))
   animal_milk_horse = db.Column(db.Numeric(30, 1))
   animal_milkrate_horse = db.Column(db.Numeric(30, 1))
   animal_milk_camel = db.Column(db.Numeric(30, 1))
   animal_milkrate_camel = db.Column(db.Numeric(30, 1))
   animal_meat_total = db.Column(db.Numeric(30, 1))
   animal_meat_cow = db.Column(db.Numeric(30, 1))
   animal_meat_sheep = db.Column(db.Numeric(30, 1))
   animal_meat_horse = db.Column(db.Numeric(30, 1))
   animal_meat_pig = db.Column(db.Numeric(30, 1))
   animal_meat_camel = db.Column(db.Numeric(30, 1))
   animal_meat_chicken = db.Column(db.Numeric(30, 1))
   animal_meat_duck = db.Column(db.Numeric(30, 1))
   animal_meat_gusi = db.Column(db.Numeric(30, 1))
   animal_egg_total = db.Column(db.BigInteger)
   animal_egg_chicken = db.Column(db.BigInteger)
   animal_egg_gusi = db.Column(db.BigInteger)
   animal_egg_perepel = db.Column(db.BigInteger)
   animal_transformator = db.Column(db.BigInteger)
   animal_transformator_isused = db.Column(db.BigInteger)
   specialization_animal = db.Column(db.String(1024))
   specialization_animal_value = db.Column(db.Numeric(30, 1))
   noncx_sto = db.Column(db.BigInteger)
   noncx_sto_needs = db.Column(db.BigInteger)
   noncx_kindergarden = db.Column(db.BigInteger)
   noncx_kindergarden_needs = db.Column(db.BigInteger)
   noncx_souvenier = db.Column(db.BigInteger)
   noncx_souvenier_needs = db.Column(db.BigInteger)
   noncx_pc_service = db.Column(db.BigInteger)
   noncx_pc_service_needs = db.Column(db.BigInteger)
   noncx_store = db.Column(db.BigInteger)
   noncx_store_needs = db.Column(db.BigInteger)
   noncx_remont_bytovoi_tech = db.Column(db.BigInteger)
   noncx_remont_bytovoi_tech_needs = db.Column(db.BigInteger)
   noncx_metal = db.Column(db.BigInteger)
   noncx_metal_needs = db.Column(db.BigInteger)
   noncx_accounting = db.Column(db.BigInteger)
   noncx_accounting_needs = db.Column(db.BigInteger)
   noncx_photo = db.Column(db.BigInteger)
   noncx_photo_needs = db.Column(db.BigInteger)
   noncx_turism = db.Column(db.BigInteger)
   noncx_turism_needs = db.Column(db.BigInteger)
   noncx_rent = db.Column(db.BigInteger)
   noncx_rent_needs = db.Column(db.BigInteger)
   noncx_cargo = db.Column(db.BigInteger)
   noncx_cargo_needs = db.Column(db.BigInteger)
   noncx_massage = db.Column(db.BigInteger)
   noncx_massage_needs = db.Column(db.BigInteger)
   noncx_foodcourt = db.Column(db.BigInteger)
   noncx_foodcourt_needs = db.Column(db.BigInteger)
   noncx_cleaning = db.Column(db.BigInteger)
   noncx_cleaning_needs = db.Column(db.BigInteger)
   noncx_beuty = db.Column(db.BigInteger)
   noncx_beuty_needs = db.Column(db.BigInteger)
   noncx_carwash = db.Column(db.BigInteger)
   noncx_carwash_needs = db.Column(db.BigInteger)
   noncx_atelie = db.Column(db.BigInteger)
   noncx_atelie_needs = db.Column(db.BigInteger)
   noncx_others = db.Column(db.BigInteger)
   noncx_others_needs = db.Column(db.BigInteger)
   noncx_stroika = db.Column(db.BigInteger)
   noncx_stroika_needs = db.Column(db.BigInteger)
   noncx_mebel = db.Column(db.BigInteger)
   noncx_mebel_needs = db.Column(db.BigInteger)
   noncx_stroi_material = db.Column(db.BigInteger)
   noncx_stroi_material_needs = db.Column(db.BigInteger)
   noncx_svarka = db.Column(db.BigInteger)
   noncx_svarka_needs = db.Column(db.BigInteger)
   noncx_woodworking = db.Column(db.BigInteger)
   noncx_woodworking_needs = db.Column(db.BigInteger)
   noncx_others_uslugi = db.Column(db.BigInteger)
   noncx_others_needs_uslugi = db.Column(db.BigInteger)
   manufacture_milk = db.Column(db.Numeric(30, 1))
   manufacture_milk_needs = db.Column(db.Numeric(30, 1))
   manufacture_meat = db.Column(db.Numeric(30, 1))
   manufacture_meat_needs = db.Column(db.Numeric(30, 1))
   manufacture_vegetables = db.Column(db.Numeric(30, 1))  # Corrected typo
   manufacture_vegetables_needs = db.Column(db.Numeric(30, 1))  # Corrected typo
   manufacture_mayo = db.Column(db.Numeric(30, 1))
   manufacture_mayo_needs = db.Column(db.Numeric(30, 1))
   manufacture_fish = db.Column(db.Numeric(30, 1))
   manufacture_fish_needs = db.Column(db.Numeric(30, 1))
   manufacture_choco = db.Column(db.Numeric(30, 1))
   manufacture_choco_needs = db.Column(db.Numeric(30, 1))
   manufacture_beer = db.Column(db.Numeric(30, 1))
   manufacture_beer_needs = db.Column(db.Numeric(30, 1))
   manufacture_vodka = db.Column(db.Numeric(30, 1))
   manufacture_vodka_needs = db.Column(db.Numeric(30, 1))
   manufacture_honey = db.Column(db.Numeric(30, 1))
   manufacture_honey_needs = db.Column(db.Numeric(30, 1))
   manufacture_polufabricat = db.Column(db.Numeric(30, 1))
   manufacture_polufabricat_needs = db.Column(db.Numeric(30, 1))
   manufacture_bread = db.Column(db.Numeric(30, 1))
   manufacture_bread_needs = db.Column(db.Numeric(30, 1))
   manufacture_others = db.Column(db.Numeric(30, 1))
   manufacture_others_needs = db.Column(db.Numeric(30, 1))
   credit_amount = db.Column(db.BigInteger)
   credit_total = db.Column(db.BigInteger)
   credit_average_total = db.Column(db.BigInteger)
   credit_zalog = db.Column(db.Numeric(30, 1))
   modified_date = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone(timedelta(hours=6))), onupdate=datetime.now(timezone(timedelta(hours=6))))
   creation_date = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone(timedelta(hours=6))))

class Form_G_O(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   kato_2 = db.Column(db.String(1024))
   kato_2_name = db.Column(db.String(1024))
   kato_4 = db.Column(db.String(1024))
   kato_4_name = db.Column(db.String(1024))
   kato_6 = db.Column(db.String(1024))
   kato_6_name = db.Column(db.String(1024))
   form_year = db.Column(db.String(1024))
   labour_population = db.Column(db.BigInteger)
   labour_constant_population = db.Column(db.BigInteger)
   labour_labour = db.Column(db.BigInteger)
   labour_government_workers = db.Column(db.BigInteger)
   labour_private_labour = db.Column(db.BigInteger)
   labour_private_ogorod = db.Column(db.BigInteger)
   labour_total_econ_inactive_population = db.Column(db.BigInteger)
   labour_unemployed = db.Column(db.BigInteger)
   labour_household_size = db.Column(db.BigInteger)
   labour_average_income_family = db.Column(db.BigInteger)
   house_total_dvor = db.Column(db.BigInteger)
   house_zaselen_dvor = db.Column(db.BigInteger)
   dh_count = db.Column(db.BigInteger)
   dx_number_ogorodov = db.Column(db.BigInteger)
   dx_cx_land = db.Column(db.Numeric(30, 1))
   dx_pashnya = db.Column(db.Numeric(30, 1))
   dx_mnogoletnie = db.Column(db.Numeric(30, 1))
   dx_zelej = db.Column(db.Numeric(30, 1))
   dx_pastbishe = db.Column(db.Numeric(30, 1))
   dx_senokosy = db.Column(db.Numeric(30, 1))
   dx_ogorody = db.Column(db.Numeric(30, 1))
   dx_sad = db.Column(db.Numeric(30, 1))
   dx_urojai = db.Column(db.Numeric(30, 1))
   dx_cucumber = db.Column(db.Numeric(30, 1))
   dx_tomato = db.Column(db.Numeric(30, 1))
   dx_potato = db.Column(db.Numeric(30, 1))
   dx_kapusta = db.Column(db.Numeric(30, 1))
   dx_carrot = db.Column(db.Numeric(30, 1))
   dx_svekla = db.Column(db.Numeric(30, 1))
   dx_sweet_peper = db.Column(db.Numeric(30, 1))
   dx_baklajan = db.Column(db.Numeric(30, 1))
   dx_kabachek = db.Column(db.Numeric(30, 1))
   dx_onion = db.Column(db.Numeric(30, 1))
   dx_chesnok = db.Column(db.Numeric(30, 1))
   dx_redis = db.Column(db.Numeric(30, 1))
   dx_korm = db.Column(db.Numeric(30, 1))
   dx_fruits = db.Column(db.Numeric(30, 1))
   kx_amount = db.Column(db.BigInteger)
   kz_cx_land = db.Column(db.Numeric(30, 1))
   kx_pansya = db.Column(db.Numeric(30, 1))
   kx_mnogoletnie = db.Column(db.Numeric(30, 1))
   kx_zelej = db.Column(db.Numeric(30, 1))
   kx_pastbishe = db.Column(db.Numeric(30, 1))
   kx_senokosy = db.Column(db.Numeric(30, 1))
   kx_urojai = db.Column(db.Numeric(30, 1))
   kx_zerno = db.Column(db.Numeric(30, 1))
   kx_rice = db.Column(db.Numeric(30, 1))
   kx_maslichnye = db.Column(db.Numeric(30, 1))
   kx_korm = db.Column(db.Numeric(30, 1))
   kx_mnogoletnie_derevo = db.Column(db.Numeric(30, 1))
   kz_cx_land_reserve = db.Column(db.Numeric(30, 1))
   kx_pansya_reserve = db.Column(db.Numeric(30, 1))
   kx_mnogoletnie_reserve = db.Column(db.Numeric(30, 1))
   kx_zelej_reserve = db.Column(db.Numeric(30, 1))
   kx_pastbishe_reserve = db.Column(db.Numeric(30, 1))
   kx_senokosy_reserve = db.Column(db.Numeric(30, 1))
   infrastructure_polivochnaya_sistema_ = db.Column(db.BigInteger)
   infrastructure_polivochnaya_sistema_isused = db.Column(db.BigInteger)
   infrastructure_polivy = db.Column(db.Numeric(30, 1))
   infrastructure_mtm = db.Column(db.BigInteger)
   infrastructure_mtm_isused = db.Column(db.BigInteger)
   infrastructure_slad = db.Column(db.BigInteger)
   infrastructure_slad_isused = db.Column(db.BigInteger)
   infrastructure_garage = db.Column(db.BigInteger)
   infrastructure_garage_isused = db.Column(db.BigInteger)
   infrastructure_cycsterny = db.Column(db.BigInteger)
   infrastructure_cycsterny_isused = db.Column(db.BigInteger)
   infrastructure_transformator = db.Column(db.BigInteger)
   infrastructure_transformator_isused = db.Column(db.BigInteger)
   specialization_rastenivodstvo = db.Column(db.String(1024))
   specialization_rastenivodstvo_value = db.Column(db.Numeric(30, 1))
   animal_dvor = db.Column(db.BigInteger)
   animal_skot_bird = db.Column(db.BigInteger)
   animal_cx_land = db.Column(db.Numeric(30, 1))
   animal_pashnya = db.Column(db.Numeric(30, 1))
   animal_mnogolet = db.Column(db.Numeric(30, 1))
   animal_zalej = db.Column(db.Numeric(30, 1))
   animal_pastbisha = db.Column(db.Numeric(30, 1))
   animal_senokos = db.Column(db.Numeric(30, 1))
   animal_ogorod = db.Column(db.Numeric(30, 1))
   animal_sad = db.Column(db.Numeric(30, 1))
   animal_krs_milk = db.Column(db.BigInteger)
   animal_krs_meat = db.Column(db.BigInteger)
   animal_sheep = db.Column(db.BigInteger)
   animal_kozel = db.Column(db.BigInteger)
   animal_horse = db.Column(db.BigInteger)
   animal_camel = db.Column(db.BigInteger)
   animal_pig = db.Column(db.BigInteger)
   animal_chicken = db.Column(db.BigInteger)
   animal_gusi = db.Column(db.BigInteger)
   animal_duck = db.Column(db.BigInteger)
   animal_induk = db.Column(db.BigInteger)
   animal_mik_total = db.Column(db.Numeric(30, 1))
   animal_milk_cow = db.Column(db.Numeric(30, 1))
   animal_milkrate_cow = db.Column(db.Numeric(30, 1))
   animal_mil_kozel = db.Column(db.Numeric(30, 1))
   animal_milrate_kozel = db.Column(db.Numeric(30, 1))
   animal_milk_horse = db.Column(db.Numeric(30, 1))
   animal_milkrate_horse = db.Column(db.Numeric(30, 1))
   animal_milk_camel = db.Column(db.Numeric(30, 1))
   animal_milkrate_camel = db.Column(db.Numeric(30, 1))
   animal_meat_total = db.Column(db.Numeric(30, 1))
   animal_meat_cow = db.Column(db.Numeric(30, 1))
   animal_meat_sheep = db.Column(db.Numeric(30, 1))
   animal_meat_horse = db.Column(db.Numeric(30, 1))
   animal_meat_pig = db.Column(db.Numeric(30, 1))
   animal_meat_camel = db.Column(db.Numeric(30, 1))
   animal_meat_chicken = db.Column(db.Numeric(30, 1))
   animal_meat_duck = db.Column(db.Numeric(30, 1))
   animal_meat_gusi = db.Column(db.Numeric(30, 1))
   animal_egg_total = db.Column(db.BigInteger)
   animal_egg_chicken = db.Column(db.BigInteger)
   animal_egg_gusi = db.Column(db.BigInteger)
   animal_egg_perepel = db.Column(db.BigInteger)
   animal_transformator = db.Column(db.BigInteger)
   animal_transformator_isused = db.Column(db.BigInteger)
   specialization_animal = db.Column(db.String(1024))
   specialization_animal_value = db.Column(db.Numeric(30, 1))
   noncx_sto = db.Column(db.BigInteger)
   noncx_sto_needs = db.Column(db.BigInteger)
   noncx_kindergarden = db.Column(db.BigInteger)
   noncx_kindergarden_needs = db.Column(db.BigInteger)
   noncx_souvenier = db.Column(db.BigInteger)
   noncx_souvenier_needs = db.Column(db.BigInteger)
   noncx_pc_service = db.Column(db.BigInteger)
   noncx_pc_service_needs = db.Column(db.BigInteger)
   noncx_store = db.Column(db.BigInteger)
   noncx_store_needs = db.Column(db.BigInteger)
   noncx_remont_bytovoi_tech = db.Column(db.BigInteger)
   noncx_remont_bytovoi_tech_needs = db.Column(db.BigInteger)
   noncx_metal = db.Column(db.BigInteger)
   noncx_metal_needs = db.Column(db.BigInteger)
   noncx_accounting = db.Column(db.BigInteger)
   noncx_accounting_needs = db.Column(db.BigInteger)
   noncx_photo = db.Column(db.BigInteger)
   noncx_photo_needs = db.Column(db.BigInteger)
   noncx_turism = db.Column(db.BigInteger)
   noncx_turism_needs = db.Column(db.BigInteger)
   noncx_rent = db.Column(db.BigInteger)
   noncx_rent_needs = db.Column(db.BigInteger)
   noncx_cargo = db.Column(db.BigInteger)
   noncx_cargo_needs = db.Column(db.BigInteger)
   noncx_massage = db.Column(db.BigInteger)
   noncx_massage_needs = db.Column(db.BigInteger)
   noncx_foodcourt = db.Column(db.BigInteger)
   noncx_foodcourt_needs = db.Column(db.BigInteger)
   noncx_cleaning = db.Column(db.BigInteger)
   noncx_cleaning_needs = db.Column(db.BigInteger)
   noncx_beuty = db.Column(db.BigInteger)
   noncx_beuty_needs = db.Column(db.BigInteger)
   noncx_carwash = db.Column(db.BigInteger)
   noncx_carwash_needs = db.Column(db.BigInteger)
   noncx_atelie = db.Column(db.BigInteger)
   noncx_atelie_needs = db.Column(db.BigInteger)
   noncx_others = db.Column(db.BigInteger)
   noncx_others_needs = db.Column(db.BigInteger)
   noncx_stroika = db.Column(db.BigInteger)
   noncx_stroika_needs = db.Column(db.BigInteger)
   noncx_mebel = db.Column(db.BigInteger)
   noncx_mebel_needs = db.Column(db.BigInteger)
   noncx_stroi_material = db.Column(db.BigInteger)
   noncx_stroi_material_needs = db.Column(db.BigInteger)
   noncx_svarka = db.Column(db.BigInteger)
   noncx_svarka_needs = db.Column(db.BigInteger)
   noncx_woodworking = db.Column(db.BigInteger)
   noncx_woodworking_needs = db.Column(db.BigInteger)
   noncx_others_uslugi = db.Column(db.BigInteger)
   noncx_others_needs_uslugi = db.Column(db.BigInteger)
   manufacture_milk = db.Column(db.Numeric(30, 1))
   manufacture_milk_needs = db.Column(db.Numeric(30, 1))
   manufacture_meat = db.Column(db.Numeric(30, 1))
   manufacture_meat_needs = db.Column(db.Numeric(30, 1))
   manufacture_vegetables = db.Column(db.Numeric(30, 1))  # Corrected typo
   manufacture_vegetables_needs = db.Column(db.Numeric(30, 1))  # Corrected typo
   manufacture_mayo = db.Column(db.Numeric(30, 1))
   manufacture_mayo_needs = db.Column(db.Numeric(30, 1))
   manufacture_fish = db.Column(db.Numeric(30, 1))
   manufacture_fish_needs = db.Column(db.Numeric(30, 1))
   manufacture_choco = db.Column(db.Numeric(30, 1))
   manufacture_choco_needs = db.Column(db.Numeric(30, 1))
   manufacture_beer = db.Column(db.Numeric(30, 1))
   manufacture_beer_needs = db.Column(db.Numeric(30, 1))
   manufacture_vodka = db.Column(db.Numeric(30, 1))
   manufacture_vodka_needs = db.Column(db.Numeric(30, 1))
   manufacture_honey = db.Column(db.Numeric(30, 1))
   manufacture_honey_needs = db.Column(db.Numeric(30, 1))
   manufacture_polufabricat = db.Column(db.Numeric(30, 1))
   manufacture_polufabricat_needs = db.Column(db.Numeric(30, 1))
   manufacture_bread = db.Column(db.Numeric(30, 1))
   manufacture_bread_needs = db.Column(db.Numeric(30, 1))
   manufacture_others = db.Column(db.Numeric(30, 1))
   manufacture_others_needs = db.Column(db.Numeric(30, 1))
   credit_amount = db.Column(db.BigInteger)
   credit_total = db.Column(db.BigInteger)
   credit_average_total = db.Column(db.BigInteger)
   credit_zalog = db.Column(db.Numeric(30, 1))
   modified_date = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone(timedelta(hours=6))), onupdate=datetime.now(timezone(timedelta(hours=6))))
   creation_date = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone(timedelta(hours=6))))


class Creditor(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   user = relationship("User", backref="creditors")
   kato_2 = db.Column(db.String(300))
   kato_2_name = db.Column(db.String(300))
   kato_4 = db.Column(db.String(300))
   kato_4_name = db.Column(db.String(300))
   kato_6 = db.Column(db.String(300))
   kato_6_name = db.Column(db.String(300))
   FIO = db.Column(db.String(300))
   IIN = db.Column(db.String(12))
   gender = db.Column(db.String(10)) #selector
   family_income_month = db.Column(db.Numeric(30, 1))
   credit_goal = db.Column(db.String(300)) # selector
   credit_other_goal = db.Column(db.String(300))
   credit_amount = db.Column(db.BigInteger)
   credit_period = db.Column(db.String(300))
   zalog_avaliability = db.Column(db.String(10)) #selector (yes/no)
   zalog_name = db.Column(db.String(100)) #selector
   zalog_address = db.Column(db.String(300))
   zalog_square = db.Column(db.Numeric(30, 1))
   zalog_creation_year = db.Column(db.String(300))
   zalog_wall_material = db.Column(db.String(300))
   zalog_hoz_buildings = db.Column(db.String(10)) #selector (yes/no)
   creditor_phone = db.Column(db.String(300))


translation_data ={
    'labour_population' : 'Численность Населения',
    'labour_constant_population' : 'Из них постоянно проживающих',
    'labour_labour' : 'Рабочая сила',
    'labour_government_workers' : 'Занятое население в бюджетной сфере',
    'labour_private_labour' : 'Занятое население в частном секторе',
    'labour_private_ogorod' : 'Из них занятое население в личном подсобном хозяйстве',
    'labour_total_econ_inactive_population' : 'Лица, не входящие в состав рабочей силы',
    'labour_unemployed' : 'Безработные',
    'labour_household_size' : 'Средний размер домашних хозяйств',
    'labour_average_income_family' : 'Средний доход на одну семью, в месяц',
    'house_total_dvor' : 'Общее количество дворов (частные дома, квартиры в многоквартирном доме, точки чабана, иное',
    'house_zaselen_dvor' : 'Из них количество заселенных дворов',
    'dh_count' : 'Количество домашних хозяйств',
    'dx_number_ogorodov' : 'Количество домашних хозяйств имеющих участки (огороды, сады, приусадебные участки',
    'dx_cx_land' : 'Сельскохозяйственные угодья домашних хозяйств',
    'dx_pashnya' : 'Пашня',
    'dx_mnogoletnie' : 'Многолетние насаждения',
    'dx_zelej' : 'Залежь',
    'dx_pastbishe' : 'Пастбища',
    'dx_senokosy' : 'Сенокосы',
    'dx_ogorody' : 'Огороды',
    'dx_sad' : 'Сады',
    'dx_urojai' : 'Объем урожая сельскохозяйственных культур в домашних хозяйствах, всего',
    'dx_cucumber' : 'Огурцы',
    'dx_tomato' : 'Помидоры',
    'dx_potato' : 'Картофель',
    'dx_kapusta' : 'Капуста',
    'dx_carrot' : 'Морковь',
    'dx_svekla' : 'Свекла',
    'dx_sweet_peper' : 'Сладкий перец',
    'dx_baklajan' : 'Баклажаны',
    'dx_kabachek' : 'Кабачки',
    'dx_onion' : 'Лук',
    'dx_chesnok' : 'Чеснок',
    'dx_redis' : 'Редис',
    'dx_korm' : 'Кормовые культуры',
    'dx_fruits' : 'Культуры многолетние (плодовые, ягодные насаждения)',
    'kx_amount' : 'Количество крестьянских хозяйств',
    'kz_cx_land' : 'Сельскохозяйственные угодья крестьянских хозяйств',
    'kx_pansya' : 'Пашня',
    'kx_mnogoletnie' : 'Многолетние насаждения',
    'kx_zelej' : 'Залежь',
    'kx_pastbishe' : 'Пастбища',
    'kx_senokosy' : 'Сенокосы',
    'kx_urojai' : 'Объем урожая сельскохозяйственных культур в крестьянских хозяйствах, всего',
    'kx_zerno' : 'Зерновые и бобовые всех видов',
    'kx_rice' : 'Рис',
    'kx_maslichnye' : 'Масличные всех видов',
    'kx_korm' : 'Кормовые культуры',
    'kx_mnogoletnie_derevo' : 'Культуры многолетние (плодовые деревья, кустарники',
    'kz_cx_land_reserve' : 'Резерв увеличения земельных угодий за счет фонда неиспользуемых и/или изъятых земель',
    'kx_pansya_reserve' : 'Пашня',
    'kx_mnogoletnie_reserve' : 'Многолетние насаждения',
    'kx_zelej_reserve' : 'Залежь',
    'kx_pastbishe_reserve' : 'Пастбища',
    'kx_senokosy_reserve' : 'Сенокосы',
    'infrastructure_polivochnaya_sistema_' : 'Обеспеченность водой для полива (наличие)', # наличие
    'infrastructure_polivochnaya_sistema_isused' : 'Обеспеченность водой для полива (используется)', # использовуется
    'infrastructure_polivy' : 'Процент покрытия поливом посевных площадей',
    'infrastructure_mtm' : 'Здание МТМ (машино-тракторная мастерская (наличие)', # наличие,
    'infrastructure_mtm_isused' : 'Здание МТМ (машино-тракторная мастерская(используется)', # использовуется,
    'infrastructure_slad' : 'Склады для хранения сырья и готовой продукции (наличие)',
    'infrastructure_slad_isused' : 'Склады для хранения сырья и готовой продукции(используется)',
    'infrastructure_garage' : 'Гаражи, ангары для хранения с/х техники и автотранспорта (наличие)',
    'infrastructure_garage_isused' : 'Гаражи, ангары для хранения с/х техники и автотранспорта(используется)',
    'infrastructure_cycsterny' : 'Цистерны для хранения ГСМ (горюче-смазочные материалы) (наличие)',
    'infrastructure_cycsterny_isused' : 'Цистерны для хранения ГСМ (горюче-смазочные материалы) (используется)',
    'infrastructure_transformator' : 'Трансформаторная электро-подстанция (наличие)',
    'infrastructure_transformator_isused' : 'Трансформаторная электро-подстанция (используется)',
    'specialization_rastenivodstvo': 'Специализация растениеводства',
    'specialization_rastenivodstvo_value': 'Рассчетное значение специализации растениеводства',
    'animal_dvor' : 'Общее число дворов',
    'animal_skot_bird' : 'Из них имеет скот и птицу',
    'animal_cx_land' : 'Сельскохозяйственные угодья домашних хозяйств',
    'animal_pashnya' : 'Пашня',
    'animal_mnogolet' : 'Многолетние насаждения',
    'animal_zalej' : 'Залежь',
    'animal_pastbisha' : 'Пастбища',
    'animal_senokos' : 'Сенокосы',
    'animal_ogorod' : 'Огороды',
    'animal_sad' : 'Сады',
    'animal_krs_milk' : 'КРС молочный',
    'animal_krs_meat' : 'КРС мясной',
    'animal_sheep' : 'Овцы, бараны',
    'animal_kozel' : 'Козы, козлы',
    'animal_horse' : 'Лошади',
    'animal_camel' : 'Верблюды',
    'animal_pig' : 'Свиньи',
    'animal_chicken' : 'Куры',
    'animal_gusi' : 'Гуси',
    'animal_duck' : 'Утки',
    'animal_induk' : 'Индюки',
    'animal_mik_total' : 'Валовой надой молока, тонн в год, всего',
    'animal_milk_cow' : 'Валовой надой коровьего молока',
    'animal_milkrate_cow' : 'Доля коровьего молока',
    'animal_mil_kozel' : 'Валовой надой козьего молока',
    'animal_milrate_kozel' : 'Доля козьего молока',
    'animal_milk_horse' : 'Валовой надой кобыльего молока',
    'animal_milkrate_horse' : 'Доля молока кобыльего молока',
    'animal_milk_camel' : 'Валовой надой верблюжьего молока',
    'animal_milkrate_camel' : 'Доля верблюжьего молока',
    'animal_meat_total' : 'Валовой сбор всего мяса',
    'animal_meat_cow' : 'Говядина',
    'animal_meat_sheep' : 'Баранина',
    'animal_meat_horse' : 'Конина',
    'animal_meat_pig' : 'Свинина',
    'animal_meat_camel' : 'Верблюжатина',
    'animal_meat_chicken' : 'Куриное мясо',
    'animal_meat_duck' : 'Утиное мясо',
    'animal_meat_gusi' : 'Гусиное мясо',
    'animal_egg_total' : 'Валовой сбор яиц',
    'animal_egg_chicken' : 'Яйца куриные',
    'animal_egg_gusi' : 'Яйца гусиные',
    'animal_egg_perepel' : 'Яйца перепелиные',
    'animal_transformator' : 'Трансформаторная электро-подстанция (наличие)',
    'animal_transformator_isused' : 'Трансформаторная электро-подстанция (используется)',
    'specialization_animal' : 'Специализация животноводства',
    'specialization_animal_value': 'Рассчетное значение специализации животноводства',
    'noncx_sto' : 'Автосервис (СТО, шиномонтаж, замена автозапчастей и т.д. (единиц)', # единиц,
    'noncx_sto_needs' : 'Автосервис (СТО, шиномонтаж, замена автозапчастей и т.д. (потребность)', # потребность,
    'noncx_kindergarden' : 'Детские центры развития, репетиторские услуги, языковые курсы (единиц)',
    'noncx_kindergarden_needs' : 'Детские центры развития, репетиторские услуги, языковые курсы (потребность)',
    'noncx_souvenier' : 'Изготовление сувениров, украшений из различных материалов (единиц)',
    'noncx_souvenier_needs' : 'Изготовление сувениров, украшений из различных материалов (потребность)',
    'noncx_pc_service' : 'Компьютерные услуги (единиц)',
    'noncx_pc_service_needs' : 'Компьютерные услуги (потребность)',
    'noncx_store' : 'Магазин (минимаркет, строительных материалов, автозапчастей, одежды и обуви, орг.техники, сотовых телефонов и акссесуаров и др.) (единиц)',
    'noncx_store_needs' : 'Магазин (минимаркет, строительных материалов, автозапчастей, одежды и обуви, орг.техники, сотовых телефонов и акссесуаров и др.) (потребность)',
    'noncx_remont_bytovoi_tech' : 'Мастерская, услуги по ремонту бытовой техники, орг.техники, инструментов, замена картриджей и т.д. (единиц)',
    'noncx_remont_bytovoi_tech_needs' : 'Мастерская, услуги по ремонту бытовой техники, орг.техники, инструментов, замена картриджей и т.д. (потребность)',
    'noncx_metal' : 'Металлопластиковые изделия (единиц)',
    'noncx_metal_needs' : 'Металлопластиковые изделия (потребность)',
    'noncx_accounting' : 'Оказание профессиональных услуг - бухгалтерские, юридические, налоговые, маркетинг, реклама и т.д (единиц)',
    'noncx_accounting_needs' : 'Оказание профессиональных услуг - бухгалтерские, юридические, налоговые, маркетинг, реклама и т.д (потребность)',
    'noncx_photo' : 'Полиграфические услуги, фотосалон, услуги фото-видео съемки (единиц)',
    'noncx_photo_needs' : 'Полиграфические услуги, фотосалон, услуги фото-видео съемки (потребность)',
    'noncx_turism' : 'Туризм (гостиницы, хостелы, кемпинги, турбазы (единиц)',
    'noncx_turism_needs' : 'Туризм (гостиницы, хостелы, кемпинги, турбазы (потребность)',
    'noncx_rent' : 'Услуги аренды (автотранспортных средств, оборудования, инструментов (единиц)',
    'noncx_rent_needs' : 'Услуги аренды (автотранспортных средств, оборудования, инструментов (потребность)',
    'noncx_cargo' : 'Услуги грузовых авто (единиц)',
    'noncx_cargo_needs' : 'Услуги грузовых авто (потребность)',
    'noncx_massage' : 'Услуги массажа, косметических, лечебных и оздоровительных процедур (единиц)',
    'noncx_massage_needs' : 'Услуги массажа, косметических, лечебных и оздоровительных процедур (потребность)',
    'noncx_foodcourt' : 'Услуги общепита (кафе, фаст-фуд, бистро, кофейни и т.д.) (единиц)',
    'noncx_foodcourt_needs' : 'Услуги общепита (кафе, фаст-фуд, бистро, кофейни и т.д.) (потребность)',
    'noncx_cleaning' : 'Услуги по уборке, озеленению, клининговые услуги и т.д. (единиц)',
    'noncx_cleaning_needs' : 'Услуги по уборке, озеленению, клининговые услуги и т.д. (потребность)',
    'noncx_beuty' : 'Услуги салонов красоты (парикмахерская, ногтевой сервис, маникюр, макияж) (единиц)',
    'noncx_beuty_needs' : 'Услуги салонов красоты (парикмахерская, ногтевой сервис, маникюр, макияж) (потребность)',
    'noncx_carwash' : 'Химчистка одежды, авто, мойка ковров и т.д. (единиц)',
    'noncx_carwash_needs' : 'Химчистка одежды, авто, мойка ковров и т.д. (потребность)',
    'noncx_atelie' : 'Швейный цех, ателье, вязальный цех, пошив и ремонт одежды, национальной одежды, головных уборов, кыз жасау, предметов быта (единиц)',
    'noncx_atelie_needs' : 'Швейный цех, ателье, вязальный цех, пошив и ремонт одежды, национальной одежды, головных уборов, кыз жасау, предметов быта (потребность)',
    'noncx_others' : 'Прочие виды услуг (единиц)',
    'noncx_others_needs' : 'Прочие виды услуг (потребность)',
    'noncx_stroika' : 'Строительные услуги (единиц)',
    'noncx_stroika_needs' : 'Строительные услуги (потребность)',
    'noncx_mebel' : 'Производство мебели (единиц)',
    'noncx_mebel_needs' : 'Производство мебели (потребность)',
    'noncx_stroi_material' : 'Производство строительных материалов (единиц)',
    'noncx_stroi_material_needs' : 'Производство строительных материалов (потребность)',
    'noncx_svarka' : 'Сварочный цех (единиц)',
    'noncx_svarka_needs' : 'Сварочный цех (потребность)',
    'noncx_woodworking' : 'Деревообработка (единиц)',
    'noncx_woodworking_needs' : 'Деревообработка (потребность)',
    'noncx_others_uslugi' : 'Прочие виды промышленности (единиц)',
    'noncx_others_needs_uslugi' : 'Прочие виды промышленности (потребность)',
    'manufacture_milk' : 'Переработка молока (предприятия) (единиц)',
    'manufacture_milk_needs' : 'Переработка молока (предприятия) (потребность)',
    'manufacture_meat' : 'Переработка мяса (предприятия) (единиц)',
    'manufacture_meat_needs' : 'Переработка мяса (предприятия) (потребность)',
    'manufacture_vegetables' : 'Переработка плодов, ягод, овощей, картофеля, дикорастущего сырья (единиц)',
    'manufacture_vegetables_needs' : 'Переработка плодов, ягод, овощей, картофеля, дикорастущего сырья (потребность)',
    'manufacture_mayo' : 'Производство майонеза, растительных масел (единиц)',
    'manufacture_mayo_needs' : 'Производство майонеза, растительных масел (потребность)',
    'manufacture_fish' : 'Переработка рыбы (единиц)',
    'manufacture_fish_needs' : 'Переработка рыбы (потребность)',
    'manufacture_choco' : 'Производство кондитерских изделий (единиц)',
    'manufacture_choco_needs' : 'Производство кондитерских изделий (потребность)',
    'manufacture_beer' : 'Производство пива и безалкогольных напитков (единиц)',
    'manufacture_beer_needs' : 'Производство пива и безалкогольных напитков (потребность)',
    'manufacture_vodka' : 'Производство ликеро-водочных изделий (единиц)',
    'manufacture_vodka_needs' : 'Производство ликеро-водочных изделий (потребность)',
    'manufacture_honey' : 'Продукция из меда (единиц)',
    'manufacture_honey_needs' : 'Продукция из меда (потребность)',
    'manufacture_polufabricat' : 'Производство полуфабрикатов (пельмени, манты, вареники, замороженные продукты и пр.) (единиц)',
    'manufacture_polufabricat_needs' : 'Производство полуфабрикатов (пельмени, манты, вареники, замороженные продукты и пр.) (потребность)',
    'manufacture_bread' : 'Производство хлебобулочных изделий (единиц)',
    'manufacture_bread_needs' : 'Производство хлебобулочных изделий (потребность)',
    'manufacture_others' : 'Прочее (единиц)',
    'manufacture_others_needs' : 'Прочее (потребность)',
    'credit_amount' : 'Количество заявок по направлениям кредита',
    'credit_total' : 'Итого общая потребность в кредитах',
    'credit_average_total' : 'Средний чек по кредиту',
    'credit_zalog' : 'Количество обеспеченных залогом участников',
    'modified_date': 'Дата обновления',
    'creation_date': 'Дата создания',
}

with app.app_context():
    db.create_all()
