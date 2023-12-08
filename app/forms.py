from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User, Form, Form_old
from app import app
from sqlalchemy import distinct, column

app.app_context().push()
class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=4, max=80)])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class FilterForm(FlaskForm):
    
    kato_4 = SelectField(choices=[])
    def set_filter_choices(self, kato_4):
        choices = [(i.kato_6, i.kato_6_name) for i in Form.query.filter_by(kato_4=kato_4).order_by(Form.kato_6_name).all()]
        choices.insert(0, (kato_4, 'Все данные'))
        self.kato_4.choices = choices

    submit = SubmitField('Применить')

class FilterHistory(FlaskForm):
    history_date = SelectField(choices=[])

    def set_history_date_choices(self, id):
        choices = [(i.modified_date, i.modified_date.strftime('%Y-%m-%d %H:%M:%S')) for i in Form_old.query.filter_by(user_id=id).all()]
        choices.insert(0, ('', 'Выберите время'))
        self.history_date.choices = choices


    submit = SubmitField('Применить')

class CreditorForm(FlaskForm):
    gender_choises = [('',''), ('Женский', 'Женский'), ('Мужской', 'Мужской')]
    credit_goal_choises = [('',''), ('КРС молочный ', 'КРС молочный '), ('КРС мясной', 'КРС мясной'), ('МРС (овцы, козы)', 'МРС (овцы, козы)'), ('Лошади','Лошади'), ('Верблюды','Верблюды'), ('Свиньи','Свиньи'), ('Птица любая','Птица любая'), ('Прочие животные','Прочие животные'), ('Зерновые и бобовые всех видов','Зерновые и бобовые всех видов'), ('Масличные всех видов','Масличные всех видов'), ('Овощи, бахчевые, корнеплоды, клубнеплоды','Овощи, бахчевые, корнеплоды, клубнеплоды'), ('Плодовые деревья и кустарники','Плодовые деревья и кустарники'), ('Прочие сельхоз культуры','Прочие сельхоз культуры'), ('Другая цель кредита','Другая цель кредита')]
    zalog_avaliability_choises = [('',''), ('Да', 'Да'), ('Нет', 'Нет')]
    zalog_name_choises = [('',''), ('Квартира', 'Квартира'), ('Дом', 'Дом'), ('Временное строение', 'Временное строение'), ('Участок', 'Участок')]
    zalog_hoz_buildings_choises = [('',''), ('Да', 'Да'), ('Нет', 'Нет')]
    FIO = StringField('ФИО потенциального заемщика', validators=[DataRequired()])
    IIN = StringField('ИИН заемщика', validators=[DataRequired()])
    gender = SelectField('Пол заемщика, выберете из списка:',choices=gender_choises, validators=[DataRequired()])
    family_income_month = DecimalField('Доход семьи в месяц (только цифры)', validators=[DataRequired()])
    credit_goal = SelectField('Цель кредита, выберите из списка:', choices=credit_goal_choises, validators=[DataRequired()])
    credit_other_goal = StringField('Если выбрана "другая цель кредита" - дайте краткое пояснение - для чего нужен кредит?')
    credit_amount = IntegerField('Запрашиваемая сумма кредита', validators=[DataRequired()])
    credit_period = StringField('Срок запрашиваемого кредита', validators=[DataRequired()])
    zalog_avaliability = SelectField('Наличие залогового обеспечения', choices=zalog_avaliability_choises, validators=[DataRequired()])
    zalog_name = StringField('Наименование имущества')
    zalog_address = StringField('Адрес')
    zalog_square = DecimalField('Общая площадь')
    zalog_creation_year = StringField('Год пострйоки')
    zalog_wall_material = StringField('Материал стен')
    zalog_hoz_buildings = SelectField('Наличие хоз построек', choices=zalog_hoz_buildings_choises)
    creditor_phone = StringField('Контактный телефон заемщика', validators=[DataRequired()])

    submit = SubmitField('Отправить')

class FormDataForm(FlaskForm):
    labour_population = IntegerField('Численность Населения')
    labour_constant_population = IntegerField('Из них постоянно проживающих')
    labour_labour = IntegerField('Рабочая сила')
    labour_government_workers = IntegerField('Занятое население в бюджетной сфере')
    labour_private_labour = IntegerField('Занятое население в частном секторе')
    labour_private_ogorod = IntegerField('Из них занятое население в личном подсобном хозяйстве')
    labour_total_econ_inactive_population = IntegerField('Лица, не входящие в состав рабочей силы')
    labour_unemployed = IntegerField('Безработные')
    labour_household_size = IntegerField('Средний размер домашних хозяйств')
    labour_average_income_family = IntegerField('Средний доход на одну семью, в месяц')
    house_total_dvor = IntegerField('Общее количество дворов (частные дома, квартиры в многоквартирном доме, точки чабана, иное)')
    house_zaselen_dvor = IntegerField('Из них количество заселенных дворов')
    dh_count = IntegerField('Количество домашних хозяйств')
    dx_number_ogorodov = IntegerField('Количество домашних хозяйств имеющих участки (огороды, сады, приусадебные участки)')
    dx_cx_land = DecimalField('Сельскохозяйственные угодья домашних хозяйств')
    dx_pashnya = DecimalField('Пашня')
    dx_mnogoletnie = DecimalField('Многолетние насаждения')
    dx_zelej = DecimalField('Залежь')
    dx_pastbishe = DecimalField('Пастбища')
    dx_senokosy = DecimalField('Сенокосы')
    dx_ogorody = DecimalField('Огороды')
    dx_sad = DecimalField('Сады')
    dx_urojai = DecimalField('Объем урожая сельскохозяйственных культур в домашних хозяйствах, всего')
    dx_cucumber = DecimalField('Огурцы')
    dx_tomato = DecimalField('Помидоры')
    dx_potato = DecimalField('Картофель')
    dx_kapusta = DecimalField('Капуста')
    dx_carrot = DecimalField('Морковь')
    dx_svekla = DecimalField('Свекла')
    dx_sweet_peper = DecimalField('Сладкий перец')
    dx_baklajan = DecimalField('Баклажаны')
    dx_kabachek = DecimalField('Кабачки')
    dx_onion = DecimalField('Лук')
    dx_chesnok = DecimalField('Чеснок')
    dx_redis = DecimalField('Редис')
    dx_korm = DecimalField('Кормовые культуры')
    dx_fruits = DecimalField('Культуры многолетние (плодовые, ягодные насаждения)')
    kx_amount = IntegerField('Количество крестьянских хозяйств')
    kz_cx_land = DecimalField('Сельскохозяйственные угодья крестьянских хозяйств')
    kx_pansya = DecimalField('Пашня')
    kx_mnogoletnie = DecimalField('Многолетние насаждения')
    kx_zelej = DecimalField('Залежь')
    kx_pastbishe = DecimalField('Пастбища')
    kx_senokosy = DecimalField('Сенокосы')
    kx_urojai = DecimalField('Объем урожая сельскохозяйственных культур в крестьянских хозяйствах, всего')
    kx_zerno = DecimalField('Зерновые и бобовые всех видов')
    kx_rice = DecimalField('Рис')
    kx_maslichnye = DecimalField('Масличные всех видов')
    kx_korm = DecimalField('Кормовые культуры')
    kx_mnogoletnie_derevo = DecimalField('Культуры многолетние (плодовые деревья, кустарники)')
    kz_cx_land_reserve = DecimalField('Резерв увеличения земельных угодий за счет фонда неиспользуемых и/или изъятых земель')
    kx_pansya_reserve = DecimalField('Пашня')
    kx_mnogoletnie_reserve = DecimalField('Многолетние насаждения')
    kx_zelej_reserve = DecimalField('Залежь')
    kx_pastbishe_reserve = DecimalField('Пастбища')
    kx_senokosy_reserve = DecimalField('Сенокосы')
    infrastructure_polivochnaya_sistema_ = IntegerField('Обеспеченность водой для полива') # наличие
    infrastructure_polivochnaya_sistema_isused = IntegerField('Обеспеченность водой для полива') # использовуется
    infrastructure_polivy = DecimalField('Процент покрытия поливом посевных площадей')
    infrastructure_mtm = IntegerField('Здание МТМ (машино-тракторная мастерская)') # наличие
    infrastructure_mtm_isused = IntegerField('Здание МТМ (машино-тракторная мастерская)') # использовуется
    infrastructure_slad = IntegerField('Склады для хранения сырья и готовой продукции')
    infrastructure_slad_isused = IntegerField('Склады для хранения сырья и готовой продукции')
    infrastructure_garage = IntegerField('Гаражи, ангары для хранения с/х техники и автотранспорта')
    infrastructure_garage_isused = IntegerField('Гаражи, ангары для хранения с/х техники и автотранспорта')
    infrastructure_cycsterny = IntegerField('Цистерны для хранения ГСМ (горюче-смазочные материалы)')
    infrastructure_cycsterny_isused = IntegerField('Цистерны для хранения ГСМ (горюче-смазочные материалы)')
    infrastructure_transformator = IntegerField('Трансформаторная электро-подстанция')
    infrastructure_transformator_isused = IntegerField('Трансформаторная электро-подстанция')
    animal_dvor = IntegerField('Общее число дворов')
    animal_skot_bird = IntegerField('Из них имеет скот и птицу')
    animal_cx_land = DecimalField('Сельскохозяйственные угодья домашних хозяйств')
    animal_pashnya = DecimalField('Пашня')
    animal_mnogolet = DecimalField('Многолетние насаждения')
    animal_zalej = DecimalField('Залежь')
    animal_pastbisha = DecimalField('Пастбища')
    animal_senokos = DecimalField('Сенокосы')
    animal_ogorod = DecimalField('Огороды')
    animal_sad = DecimalField('Сады')
    animal_krs_milk = IntegerField('КРС молочный')
    animal_krs_meat = IntegerField('КРС мясной')
    animal_sheep = IntegerField('Овцы, бараны')
    animal_kozel = IntegerField('Козы, козлы')
    animal_horse = IntegerField('Лошади')
    animal_camel = IntegerField('Верблюды')
    animal_pig = IntegerField('Свиньи')
    animal_chicken = IntegerField('Куры')
    animal_gusi = IntegerField('Гуси')
    animal_duck = IntegerField('Утки')
    animal_induk = IntegerField('Индюки')
    animal_mik_total = DecimalField('Валовой надой молока, тонн в год, всего')
    animal_milk_cow = DecimalField('Валовой надой коровьего молока')
    animal_milkrate_cow = DecimalField('Доля коровьего молока')
    animal_mil_kozel = DecimalField('Валовой надой козьего молока')
    animal_milrate_kozel = DecimalField('Доля козьего молока')
    animal_milk_horse = DecimalField('Валовой надой кобыльего молока')
    animal_milkrate_horse = DecimalField('Доля молока кобыльего молока')
    animal_milk_camel = DecimalField('Валовой надой верблюжьего молока')
    animal_milkrate_camel = DecimalField('Доля верблюжьего молока')
    animal_meat_total = DecimalField('Валовой сбор всего мяса')
    animal_meat_cow = DecimalField('Говядина')
    animal_meat_sheep = DecimalField('Баранина')
    animal_meat_horse = DecimalField('Конина')
    animal_meat_pig = DecimalField('Свинина')
    animal_meat_camel = DecimalField('Верблюжатина')
    animal_meat_chicken = DecimalField('Куриное мясо')
    animal_meat_duck = DecimalField('Утиное мясо')
    animal_meat_gusi = DecimalField('Гусиное мясо')
    animal_egg_total = IntegerField('Валовой сбор яиц')
    animal_egg_chicken = IntegerField('Яйца куриные')
    animal_egg_gusi = IntegerField('Яйца гусиные')
    animal_egg_perepel = IntegerField('Яйца перепелиные')
    animal_transformator = IntegerField('Трансформаторная электро-подстанция')
    animal_transformator_isused = IntegerField('Трансформаторная электро-подстанция')
    noncx_sto = IntegerField('Автосервис (СТО, шиномонтаж, замена автозапчастей и т.д.)') # единиц
    noncx_sto_needs = IntegerField('Автосервис (СТО, шиномонтаж, замена автозапчастей и т.д.)') # потребитель
    noncx_kindergarden = IntegerField('Детские центры развития, репетиторские услуги, языковые курсы')
    noncx_kindergarden_needs = IntegerField('Детские центры развития, репетиторские услуги, языковые курсы')
    noncx_souvenier = IntegerField('Изготовление сувениров, украшений из различных материалов')
    noncx_souvenier_needs = IntegerField('Изготовление сувениров, украшений из различных материалов')
    noncx_pc_service = IntegerField('Компьютерные услуги')
    noncx_pc_service_needs = IntegerField('Компьютерные услуги')
    noncx_store = IntegerField('Магазин (минимаркет, строительных материалов, автозапчастей, одежды и обуви, орг.техники, сотовых телефонов и акссесуаров и др.)')
    noncx_store_needs = IntegerField('Магазин (минимаркет, строительных материалов, автозапчастей, одежды и обуви, орг.техники, сотовых телефонов и акссесуаров и др.)')
    noncx_remont_bytovoi_tech = IntegerField('Мастерская, услуги по ремонту бытовой техники, орг.техники, инструментов, замена картриджей и т.д.')
    noncx_remont_bytovoi_tech_needs = IntegerField('Мастерская, услуги по ремонту бытовой техники, орг.техники, инструментов, замена картриджей и т.д.')
    noncx_metal = IntegerField('Металлопластиковые изделия')
    noncx_metal_needs = IntegerField('Металлопластиковые изделия')
    noncx_accounting = IntegerField('Оказание профессиональных услуг - бухгалтерские, юридические, налоговые, маркетинг, реклама и т.д')
    noncx_accounting_needs = IntegerField('Оказание профессиональных услуг - бухгалтерские, юридические, налоговые, маркетинг, реклама и т.д')
    noncx_photo = IntegerField('Полиграфические услуги, фотосалон, услуги фото-видео съемки')
    noncx_photo_needs = IntegerField('Полиграфические услуги, фотосалон, услуги фото-видео съемки')
    noncx_turism = IntegerField('Туризм (гостиницы, хостелы, кемпинги, турбазы)')
    noncx_turism_needs = IntegerField('Туризм (гостиницы, хостелы, кемпинги, турбазы)')
    noncx_rent = IntegerField('Услуги аренды (автотранспортных средств, оборудования, инструментов)')
    noncx_rent_needs = IntegerField('Услуги аренды (автотранспортных средств, оборудования, инструментов)')
    noncx_cargo = IntegerField('Услуги грузовых авто')
    noncx_cargo_needs = IntegerField('Услуги грузовых авто')
    noncx_massage = IntegerField('Услуги массажа, косметических, лечебных и оздоровительных процедур')
    noncx_massage_needs = IntegerField('Услуги массажа, косметических, лечебных и оздоровительных процедур')
    noncx_foodcourt = IntegerField('Услуги общепита (кафе, фаст-фуд, бистро, кофейни и т.д.)')
    noncx_foodcourt_needs = IntegerField('Услуги общепита (кафе, фаст-фуд, бистро, кофейни и т.д.)')
    noncx_cleaning = IntegerField('Услуги по уборке, озеленению, клининговые услуги и т.д.')
    noncx_cleaning_needs = IntegerField('Услуги по уборке, озеленению, клининговые услуги и т.д.')
    noncx_beuty = IntegerField('Услуги салонов красоты (парикмахерская, ногтевой сервис, маникюр, макияж)')
    noncx_beuty_needs = IntegerField('Услуги салонов красоты (парикмахерская, ногтевой сервис, маникюр, макияж)')
    noncx_carwash = IntegerField('Химчистка одежды, авто, мойка ковров и т.д.')
    noncx_carwash_needs = IntegerField('Химчистка одежды, авто, мойка ковров и т.д.')
    noncx_atelie = IntegerField('Швейный цех, ателье, вязальный цех, пошив и ремонт одежды, национальной одежды, головных уборов, кыз жасау, предметов быта')
    noncx_atelie_needs = IntegerField('Швейный цех, ателье, вязальный цех, пошив и ремонт одежды, национальной одежды, головных уборов, кыз жасау, предметов быта')
    noncx_others = IntegerField('Прочие виды услуг')
    noncx_others_needs = IntegerField('Прочие виды услуг')
    noncx_stroika = IntegerField('Строительные услуги')
    noncx_stroika_needs = IntegerField('Строительные услуги')
    noncx_mebel = IntegerField('Производство мебели')
    noncx_mebel_needs = IntegerField('Производство мебели')
    noncx_stroi_material = IntegerField('Производство строительных материалов')
    noncx_stroi_material_needs = IntegerField('Производство строительных материалов')
    noncx_svarka = IntegerField('Сварочный цех')
    noncx_svarka_needs = IntegerField('Сварочный цех')
    noncx_woodworking = IntegerField('Деревообработка')
    noncx_woodworking_needs = IntegerField('Деревообработка')
    noncx_others_uslugi = IntegerField('Прочие виды промышленности')
    noncx_others_needs_uslugi = IntegerField('Прочие виды промышленности')
    manufacture_milk = DecimalField('Переработка молока (предприятия)')
    manufacture_milk_needs = DecimalField('Переработка молока (предприятия)')
    manufacture_meat = DecimalField('Переработка мяса (предприятия)')
    manufacture_meat_needs = DecimalField('Переработка мяса (предприятия)')
    manufacture_vegetables = DecimalField('Переработка плодов, ягод, овощей, картофеля, дикорастущего сырья')
    manufacture_vegetables_needs = DecimalField('Переработка плодов, ягод, овощей, картофеля, дикорастущего сырья')
    manufacture_mayo = DecimalField('Производство майонеза, растительных масел')
    manufacture_mayo_needs = DecimalField('Производство майонеза, растительных масел')
    manufacture_fish = DecimalField('Переработка рыбы')
    manufacture_fish_needs = DecimalField('Переработка рыбы')
    manufacture_choco = DecimalField('Производство кондитерских изделий')
    manufacture_choco_needs = DecimalField('Производство кондитерских изделий')
    manufacture_beer = DecimalField('Производство пива и безалкогольных напитков')
    manufacture_beer_needs = DecimalField('Производство пива и безалкогольных напитков')
    manufacture_vodka = DecimalField('Производство ликеро-водочных изделий')
    manufacture_vodka_needs = DecimalField('Производство ликеро-водочных изделий')
    manufacture_honey = DecimalField('Продукция из меда')
    manufacture_honey_needs = DecimalField('Продукция из меда')
    manufacture_polufabricat = DecimalField('Производство полуфабрикатов (пельмени, манты, вареники, замороженные продукты и пр.)')
    manufacture_polufabricat_needs = DecimalField('Производство полуфабрикатов (пельмени, манты, вареники, замороженные продукты и пр.)')
    manufacture_bread = DecimalField('Производство хлебобулочных изделий')
    manufacture_bread_needs = DecimalField('Производство хлебобулочных изделий')
    manufacture_others = DecimalField('Прочее')
    manufacture_others_needs = DecimalField('Прочее')
    credit_amount = IntegerField('Количество заявок по направлениям кредита')
    credit_total = IntegerField('Итого общая потребность в кредитах')
    credit_average_total = IntegerField('Средний чек по кредиту')
    credit_zalog = DecimalField('Количество обеспеченных залогом участников') # %

    #specializations
    specialization_rastenivodstvo_weat = BooleanField('Пшеница')
    specialization_rastenivodstvo_corn = BooleanField('Кукуруза')
    specialization_rastenivodstvo_barely = BooleanField('Ячмень')
    specialization_rastenivodstvo_millet = BooleanField('Просо')
    specialization_rastenivodstvo_hay = BooleanField('Сено')
    specialization_rastenivodstvo_lucerne = BooleanField('Люцерна')
    specialization_rastenivodstvo_sunflower = BooleanField('Подсолнечник')
    specialization_rastenivodstvo_rasp = BooleanField('Расп')
    specialization_rastenivodstvo_sorghum = BooleanField('Сорго')
    specialization_rastenivodstvo_green_beans = BooleanField('Фасоль зеленая')
    specialization_rastenivodstvo_green_peas = BooleanField('Горох зеленый')
    specialization_rastenivodstvo_soybeans = BooleanField('Бобы соевые')
    specialization_rastenivodstvo_ground_nuts = BooleanField('Орехи земляные')
    specialization_rastenivodstvo_almond = BooleanField('Миндаль')
    specialization_rastenivodstvo_forest_nuts = BooleanField('Орехи лесные')
    specialization_rastenivodstvo_pistachios = BooleanField('Фисташки')
    specialization_rastenivodstvo_walnuts = BooleanField('Орехи грецкие')
    specialization_rastenivodstvo_rice = BooleanField('Рис')
    specialization_rastenivodstvo_cabbage = BooleanField('Капуста')
    specialization_rastenivodstvo_cauliflower_and_broccoli = BooleanField('Капуста цветная и брокколи')
    specialization_rastenivodstvo_spinach = BooleanField('Шпинат')
    specialization_rastenivodstvo_watermelons = BooleanField('Арбузы')
    specialization_rastenivodstvo_melon = BooleanField('Дыня')
    specialization_rastenivodstvo_chili_and_peppers = BooleanField('Чили и перцы')
    specialization_rastenivodstvo_eggplants = BooleanField('Баклажаны')
    specialization_rastenivodstvo_zucchini = BooleanField('Кабачки')
    specialization_rastenivodstvo_radish = BooleanField('Редис')
    specialization_rastenivodstvo_tomatoes = BooleanField('Помидоры')
    specialization_rastenivodstvo_cucumbers = BooleanField('Огурцы')
    specialization_rastenivodstvo_carrot = BooleanField('Морковь')
    specialization_rastenivodstvo_garlic = BooleanField('Чеснок')
    specialization_rastenivodstvo_onion = BooleanField('Лук')
    specialization_rastenivodstvo_potatoes = BooleanField('Картофель')
    specialization_rastenivodstvo_sweet_potatoes = BooleanField('Картофель сладкий')
    specialization_rastenivodstvo_sugar_beet = BooleanField('Свекла сахарная')
    specialization_rastenivodstvo_mushrooms_and_truffles = BooleanField('Грибы и трюфели')
    specialization_rastenivodstvo_grapes = BooleanField('Виноград')
    specialization_rastenivodstvo_lemons_and_limes = BooleanField('Лимоны и лаймы')
    specialization_rastenivodstvo_apples = BooleanField('Яблоки')
    specialization_rastenivodstvo_pears = BooleanField('Груши')
    specialization_rastenivodstvo_quince = BooleanField('Айва')
    specialization_rastenivodstvo_apricots = BooleanField('Абрикосы')
    specialization_rastenivodstvo_cherry = BooleanField('Вишня')
    specialization_rastenivodstvo_peaches = BooleanField('Персики')
    specialization_rastenivodstvo_plums = BooleanField('Сливы')
    specialization_rastenivodstvo_raspberry = BooleanField('Малина')
    specialization_rastenivodstvo_strawberry = BooleanField('Земляника (клубника)')
    specialization_rastenivodstvo_currant = BooleanField('Смородина')
    specialization_rastenivodstvo_others = BooleanField('Другое')

    specialization_animal_cow_milk = BooleanField('Молоко коровье')
    specialization_animal_goat_milk = BooleanField('Молоко козье')
    specialization_animal_horse_milk = BooleanField('Молоко кобылье')
    specialization_animal_camel_milk = BooleanField('Верблюжье молоко')
    specialization_animal_beef = BooleanField('Говядина')
    specialization_animal_sheepmeat = BooleanField('Баранина')
    specialization_animal_horse_meat= BooleanField('Конина')
    specialization_animal_pork= BooleanField('Свинина')
    specialization_animal_camel_meat= BooleanField('Верблюжатина')
    specialization_animal_chicken_meat= BooleanField('Мясо куриное')
    specialization_animal_duck_meat= BooleanField('Мясо утиное')
    specialization_animal_goose_meat= BooleanField('Мясо гусиное')
    specialization_animal_chicken_egg = BooleanField('Яйцо куриное')
    specialization_animal_goose_egg = BooleanField('Яйцо гусиное')
    specialization_animal_quail_egg = BooleanField('Яйцо перепелиное')

    submit = SubmitField('Сохранить')
