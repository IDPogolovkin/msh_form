from app import app, db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from datetime import timedelta, datetime, timezone

@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))

class User(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key = True)
   kato_2 = db.Column(db.String(20))
   kato_2_name = db.Column(db.String(20))
   kato_4 = db.Column(db.String(20))
   kato_4_name = db.Column(db.String(20)) 
   kato_6 = db.Column(db.String(20))
   kato_6_name = db.Column(db.String(20))
   password = db.Column(db.String(250))
   def __repr__(self):
      return f"KATO_2('{self.kato_2}'), KATO_4('{self.kato_4}'),  KATO_6('{self.kato_6}')"

class Form(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   user = relationship("User",backref="forms") 
   kato_2 = db.Column(db.String(20))
   kato_2_name = db.Column(db.String(20))
   kato_4 = db.Column(db.String(20))
   kato_4_name = db.Column(db.String(20)) 
   kato_6 = db.Column(db.String(20))
   kato_6_name = db.Column(db.String(20))
   form_year = db.Column(db.String(10))
   labour_population = db.Column(db.Integer)
   labour_constant_population = db.Column(db.Integer)
   labour_labour = db.Column(db.Integer)
   labour_government_workers = db.Column(db.Integer)
   labour_private_labour = db.Column(db.Integer)
   labour_private_ogorod = db.Column(db.Integer)
   labour_total_econ_inactive_population = db.Column(db.Integer)
   labour_unemployed = db.Column(db.Integer)
   labour_household_size = db.Column(db.Integer)
   labour_average_income_family = db.Column(db.Integer)
   house_total_dvor = db.Column(db.Integer)
   house_zaselen_dvor = db.Column(db.Integer)
   dh_count = db.Column(db.Integer)
   dx_number_ogorodov = db.Column(db.Integer)
   dx_cx_land = db.Column(db.Numeric(30, 2))
   dx_pashnya = db.Column(db.Numeric(30, 2))
   dx_mnogoletnie = db.Column(db.Numeric(30, 2))
   dx_zelej = db.Column(db.Numeric(30, 2))
   dx_pastbishe = db.Column(db.Numeric(30, 2))
   dx_senokosy = db.Column(db.Numeric(30, 2))
   dx_ogorody = db.Column(db.Numeric(30, 2))
   dx_sad = db.Column(db.Numeric(30, 2))
   dx_urojai = db.Column(db.Numeric(30, 2))
   dx_cucumber = db.Column(db.Numeric(30, 2))
   dx_tomato = db.Column(db.Numeric(30, 2))
   dx_potato = db.Column(db.Numeric(30, 2))
   dx_kapusta = db.Column(db.Numeric(30, 2))
   dx_carrot = db.Column(db.Numeric(30, 2))
   dx_svekla = db.Column(db.Numeric(30, 2))
   dx_sweet_peper = db.Column(db.Numeric(30, 2))
   dx_baklajan = db.Column(db.Numeric(30, 2))
   dx_kabachek = db.Column(db.Numeric(30, 2))
   dx_onion = db.Column(db.Numeric(30, 2))
   dx_chesnok = db.Column(db.Numeric(30, 2))
   dx_redis = db.Column(db.Numeric(30, 2))
   dx_korm = db.Column(db.Numeric(30, 2))
   dx_fruits = db.Column(db.Numeric(30, 2))
   kx_amount = db.Column(db.Integer)
   kz_cx_land = db.Column(db.Numeric(30, 2))
   kx_pansya = db.Column(db.Numeric(30, 2))
   kx_mnogoletnie = db.Column(db.Numeric(30, 2))
   kx_zelej = db.Column(db.Numeric(30, 2))
   kx_pastbishe = db.Column(db.Numeric(30, 2))
   kx_senokosy = db.Column(db.Numeric(30, 2))
   kx_urojai = db.Column(db.Numeric(30, 2))
   kx_zerno = db.Column(db.Numeric(30, 2))
   kx_rice = db.Column(db.Numeric(30, 2))
   kx_maslichnye = db.Column(db.Numeric(30, 2))
   kx_korm = db.Column(db.Numeric(30, 2))
   kx_mnogoletnie_derevo = db.Column(db.Numeric(30, 2))
   kz_cx_land_reserve = db.Column(db.Numeric(30, 2))
   kx_pansya_reserve = db.Column(db.Numeric(30, 2))
   kx_mnogoletnie_reserve = db.Column(db.Numeric(30, 2))
   kx_zelej_reserve = db.Column(db.Numeric(30, 2))
   kx_pastbishe_reserve = db.Column(db.Numeric(30, 2))
   kx_senokosy_reserve = db.Column(db.Numeric(30, 2))
   infrastructure_polivochnaya_sistema_ = db.Column(db.Integer)
   infrastructure_polivochnaya_sistema_isused = db.Column(db.Integer)
   infrastructure_polivy = db.Column(db.Numeric(30, 2))
   infrastructure_mtm = db.Column(db.Integer)
   infrastructure_mtm_isused = db.Column(db.Integer)
   infrastructure_slad = db.Column(db.Integer)
   infrastructure_slad_isused = db.Column(db.Integer)
   infrastructure_garage = db.Column(db.Integer)
   infrastructure_garage_isused = db.Column(db.Integer)
   infrastructure_cycsterny = db.Column(db.Integer)
   infrastructure_cycsterny_isused = db.Column(db.Integer)
   infrastructure_transformator = db.Column(db.Integer)
   infrastructure_transformator_isused = db.Column(db.Integer)
   specialization_rastenivodstvo = db.Column(db.String(300))
   animal_dvor = db.Column(db.Integer)
   animal_skot_bird = db.Column(db.Integer)
   animal_cx_land = db.Column(db.Numeric(30, 2))
   animal_pashnya = db.Column(db.Numeric(30, 2))
   animal_mnogolet = db.Column(db.Numeric(30, 2))
   animal_zalej = db.Column(db.Numeric(30, 2))
   animal_pastbisha = db.Column(db.Numeric(30, 2))
   animal_senokos = db.Column(db.Numeric(30, 2))
   animal_ogorod = db.Column(db.Numeric(30, 2))
   animal_sad = db.Column(db.Numeric(30, 2))
   animal_krs_milk = db.Column(db.Integer)
   animal_krs_meat = db.Column(db.Integer)
   animal_sheep = db.Column(db.Integer)
   animal_kozel = db.Column(db.Integer)
   animal_horse = db.Column(db.Integer)
   animal_camel = db.Column(db.Integer)
   animal_pig = db.Column(db.Integer)
   animal_chicken = db.Column(db.Integer)
   animal_gusi = db.Column(db.Integer)
   animal_duck = db.Column(db.Integer)
   animal_induk = db.Column(db.Integer)
   animal_mik_total = db.Column(db.Numeric(30, 2))
   animal_milk_cow = db.Column(db.Numeric(30, 2))
   animal_milkrate_cow = db.Column(db.Numeric(30, 2))
   animal_mil_kozel = db.Column(db.Numeric(30, 2))
   animal_milrate_kozel = db.Column(db.Numeric(30, 2))
   animal_milk_horse = db.Column(db.Numeric(30, 2))
   animal_milkrate_horse = db.Column(db.Numeric(30, 2))
   animal_milk_camel = db.Column(db.Numeric(30, 2))
   animal_milkrate_camel = db.Column(db.Numeric(30, 2))
   animal_meat_total = db.Column(db.Numeric(30, 2))
   animal_meat_cow = db.Column(db.Numeric(30, 2))
   animal_meat_sheep = db.Column(db.Numeric(30, 2))
   animal_meat_horse = db.Column(db.Numeric(30, 2))
   animal_meat_pig = db.Column(db.Numeric(30, 2))
   animal_meat_camel = db.Column(db.Numeric(30, 2))
   animal_meat_chicken = db.Column(db.Numeric(30, 2))
   animal_meat_duck = db.Column(db.Numeric(30, 2))
   animal_meat_gusi = db.Column(db.Numeric(30, 2))
   animal_egg_total = db.Column(db.Integer)
   animal_egg_chicken = db.Column(db.Integer)
   animal_egg_gusi = db.Column(db.Integer)
   animal_egg_perepel = db.Column(db.Integer)
   animal_transformator = db.Column(db.Integer)
   animal_transformator_isused = db.Column(db.Integer)
   specialization_animal = db.Column(db.String(300))
   noncx_sto = db.Column(db.Integer)
   noncx_sto_needs = db.Column(db.Integer)
   noncx_kindergarden = db.Column(db.Integer)
   noncx_kindergarden_needs = db.Column(db.Integer)
   noncx_souvenier = db.Column(db.Integer)
   noncx_souvenier_needs = db.Column(db.Integer)
   noncx_pc_service = db.Column(db.Integer)
   noncx_pc_service_needs = db.Column(db.Integer)
   noncx_store = db.Column(db.Integer)
   noncx_store_needs = db.Column(db.Integer)
   noncx_remont_bytovoi_tech = db.Column(db.Integer)
   noncx_remont_bytovoi_tech_needs = db.Column(db.Integer)
   noncx_metal = db.Column(db.Integer)
   noncx_metal_needs = db.Column(db.Integer)
   noncx_accounting = db.Column(db.Integer)
   noncx_accounting_needs = db.Column(db.Integer)
   noncx_photo = db.Column(db.Integer)
   noncx_photo_needs = db.Column(db.Integer)
   noncx_turism = db.Column(db.Integer)
   noncx_turism_needs = db.Column(db.Integer)
   noncx_rent = db.Column(db.Integer)
   noncx_rent_needs = db.Column(db.Integer)
   noncx_cargo = db.Column(db.Integer)
   noncx_cargo_needs = db.Column(db.Integer)
   noncx_massage = db.Column(db.Integer)
   noncx_massage_needs = db.Column(db.Integer)
   noncx_foodcourt = db.Column(db.Integer)
   noncx_foodcourt_needs = db.Column(db.Integer)
   noncx_cleaning = db.Column(db.Integer)
   noncx_cleaning_needs = db.Column(db.Integer)
   noncx_beuty = db.Column(db.Integer)
   noncx_beuty_needs = db.Column(db.Integer)
   noncx_carwash = db.Column(db.Integer)
   noncx_carwash_needs = db.Column(db.Integer)
   noncx_atelie = db.Column(db.Integer)
   noncx_atelie_needs = db.Column(db.Integer)
   noncx_others = db.Column(db.Integer)
   noncx_others_needs = db.Column(db.Integer)
   noncx_stroika = db.Column(db.Integer)
   noncx_stroika_needs = db.Column(db.Integer)
   noncx_mebel = db.Column(db.Integer)
   noncx_mebel_needs = db.Column(db.Integer)
   noncx_stroi_material = db.Column(db.Integer)
   noncx_stroi_material_needs = db.Column(db.Integer)
   noncx_svarka = db.Column(db.Integer)
   noncx_svarka_needs = db.Column(db.Integer)
   noncx_woodworking = db.Column(db.Integer)
   noncx_woodworking_needs = db.Column(db.Integer)
   noncx_others_uslugi = db.Column(db.Integer)
   noncx_others_needs_uslugi = db.Column(db.Integer)
   manufacture_milk = db.Column(db.Numeric(30, 2))
   manufacture_milk_needs = db.Column(db.Numeric(30, 2))
   manufacture_meat = db.Column(db.Numeric(30, 2))
   manufacture_meat_needs = db.Column(db.Numeric(30, 2))
   manufacture_vegetables = db.Column(db.Numeric(30, 2))  # Corrected typo
   manufacture_vegetables_needs = db.Column(db.Numeric(30, 2))  # Corrected typo
   manufacture_mayo = db.Column(db.Numeric(30, 2))
   manufacture_mayo_needs = db.Column(db.Numeric(30, 2))
   manufacture_fish = db.Column(db.Numeric(30, 2))
   manufacture_fish_needs = db.Column(db.Numeric(30, 2))
   manufacture_choco = db.Column(db.Numeric(30, 2))
   manufacture_choco_needs = db.Column(db.Numeric(30, 2))
   manufacture_beer = db.Column(db.Numeric(30, 2))
   manufacture_beer_needs = db.Column(db.Numeric(30, 2))
   manufacture_vodka = db.Column(db.Numeric(30, 2))
   manufacture_vodka_needs = db.Column(db.Numeric(30, 2))
   manufacture_honey = db.Column(db.Numeric(30, 2))
   manufacture_honey_needs = db.Column(db.Numeric(30, 2))
   manufacture_polufabricat = db.Column(db.Numeric(30, 2))
   manufacture_polufabricat_needs = db.Column(db.Numeric(30, 2))
   manufacture_bread = db.Column(db.Numeric(30, 2))
   manufacture_bread_needs = db.Column(db.Numeric(30, 2))
   manufacture_others = db.Column(db.Numeric(30, 2))
   manufacture_others_needs = db.Column(db.Numeric(30, 2))
   credit_amount = db.Column(db.Integer)
   credit_total = db.Column(db.Integer)
   credit_average_total = db.Column(db.Integer)
   credit_zalog = db.Column(db.Numeric(30, 2))
   modified_date = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone(timedelta(hours=6))), onupdate=datetime.now(timezone(timedelta(hours=6))))
   creation_date = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone(timedelta(hours=6))))

class Creditor(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   user_kato = db.Column(db.String(50), db.ForeignKey('user.kato_6'))
   user = relationship("User",backref="creditors") 
   kato_2 = db.Column(db.String(20), )
   kato_2_name = db.Column(db.String(20), )
   kato_4 = db.Column(db.String(20), )
   kato_4_name = db.Column(db.String(20), ) 
   kato_6 = db.Column(db.String(20), )
   kato_6_name = db.Column(db.String(20), )
   FIO = db.Column(db.String(20))
   IIN = db.Column(db.String(12))
   gender = db.Column(db.String(10)) #selector
   family_income_month = db.Column(db.Numeric(30, 2))
   credit_goal = db.Column(db.String(300)) # selector
   credit_other_goal = db.Column(db.String(300))
   credit_amount = db.Column(db.Integer)
   credit_period = db.Column(db.String(100))
   zalog_avaliability = db.Column(db.String(10)) #selector (yes/no)
   zalog_name = db.Column(db.String(100)) #selector
   zalog_address = db.Column(db.String(100)) 
   zalog_square = db.Column(db.Numeric(30, 2))
   zalog_creation_year = db.Column(db.String(50))
   zalog_wall_material = db.Column(db.String(300))
   zalog_hoz_buildings = db.Column(db.String(10)) #selector (yes/no)


with app.app_context():
    db.create_all()
