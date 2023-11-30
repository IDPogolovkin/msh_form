from flask import flash, redirect, render_template, url_for, request
from app.forms import *
from app.models import *
from app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from decimal import Decimal
from sqlalchemy import desc
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, select, types
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.sql import func, text
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import aliased
from sqlalchemy import func, and_
from sqlalchemy.inspection import inspect
import statistics


Base = declarative_base()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

measurement_units = {
    'human': 'человек',
    'tg/m': 'тенге/месяц',
    'unit': 'единиц',
    'square': 'кв.метров',
    't/y': 'тонн/год',
    'gectar':'гектар',
    'a':'в наличии',
    'used': 'используется',
    'heads':'голов',
    '%':'%',
    't_p/y':'тыс. штук/год',
    'p/y':'штук/год',
    'c':'потребность',
    'tenge':'тенге',
}

# @app.route('/')
# def home():
#     return render_template('base.html', user=current_user)

@app.route('/',  methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        if current_user.is_district:
            return redirect(url_for('region_akim'))
            
        else:
            formData=Form.query.filter_by(user_id=current_user.id).first()
            if formData:
                return redirect(url_for('edit_form'))
            else:
                return redirect(url_for('form_village'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('login'))
        else:
             flash('Неверный логин или пароль! Попробуйте еще раз', category='error')
    return render_template('login.html', title='Login', form=form, user=current_user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    filterhistory = FilterHistory()
    form = FormDataForm()
    filterhistory.set_history_date_choices(current_user.id)
    if request.method == 'GET':
        # print(formdata)

        return render_template('account.html', title = 'Личный кабинет', filterhistory=filterhistory,str=str,form=form,measurement_units=measurement_units, user=current_user)
    else:
        if filterhistory.history_date.data != '':
            formdata = Form_old.query.filter_by(user_id=current_user.id).order_by(text(f"modified_date = '{filterhistory.history_date.data}' DESC")).first()
        else:
            return redirect(url_for('account'))
        return render_template('account.html', title = 'Личный кабинет', filterhistory=filterhistory,str=str,form=form,measurement_units=measurement_units, user=current_user, formdata=formdata)
    

@app.route('/account/edit', methods=['POST', 'GET'])
@login_required
def edit_form():
    formdata = Form.query.filter_by(user_id=current_user.id).first()
    form = FormDataForm(obj=formdata)
    formgo = Form_G_O.query.filter_by(kato_6=current_user.kato_6).first()

    if request.method == 'GET':
        return render_template('edit_form.html',str=str, form=form, formGO = formgo, user=current_user, measurement_units=measurement_units, formData=formdata)
    else:

        if form.validate_on_submit():
            old_form_columns = [column.key for column in inspect(Form_old).columns]
            old_form_data = {column: getattr(formdata, column) for column in old_form_columns}
            old_form = Form_old(**old_form_data)
            form_data = form.data
            model_columns = Form.__table__.columns.keys()
            form_data = {key: value for key, value in form_data.items() if key in model_columns}
            for key, value in form_data.items():
                if isinstance(value, Decimal):
                    form_data[key] = float(value)
            spec_str_rast = ''
            for field in form:
                if field.name.startswith('specialization_rastenivodstvo_'):
                    if field.data == True:
                        spec_str_rast += str(field.label.text) + ', '
            spec_str_animal = ''
            for field in form:
                if field.name.startswith('specialization_animal_'):
                    if field.data == True:
                        spec_str_animal += str(field.label.text) + ', '
            new_form = Form(**form_data)
            new_form.kato_2 = current_user.kato_2
            new_form.kato_2_name = current_user.kato_2_name
            new_form.kato_4 = current_user.kato_4
            new_form.kato_4_name = current_user.kato_4_name
            new_form.kato_6 = current_user.kato_6
            new_form.kato_6_name = current_user.kato_6_name
            new_form.user_id = current_user.id
            new_form.form_year = datetime.now().year
            new_form.creation_date = datetime.now(timezone(timedelta(hours=6)))
            new_form.modified_date = datetime.now(timezone(timedelta(hours=6)))
            new_form.specialization_animal = spec_str_animal[:-2]
            new_form.specialization_rastenivodstvo = spec_str_rast[:-2]
            formdata.modified_date = datetime.now(timezone(timedelta(hours=6)))
            db.session.delete(formdata)
            db.session.add(new_form)
            db.session.add(old_form)
            db.session.commit()
            flash("Данные успешно изменены!", 'success')
            return redirect(url_for('edit_form'))
        else:
            print(form.errors)
            flash("Данные не изменены! Некорректный формат.", 'danger')
            return render_template('edit_form.html',formGO = formgo,measurement_units=measurement_units, form=form, user=current_user)

@app.route('/account/region', methods=['GET', 'POST'])
@login_required
def region_akim():

    filterform = FilterForm()
    filterform.set_filter_choices(current_user.kato_4)
    inspector1 = inspect(Form)
    inspector2 = inspect(Form_G_O)
    columns = inspector1.columns.keys()
    columnsgo = inspector2.columns.keys()
    
    formdata_list = Form.query.filter_by(kato_4=current_user.kato_4).all()
    formgo_list = Form_G_O.query.filter_by(kato_4=current_user.kato_4).all()
    count_form = len(formdata_list)
    count_form_go = len(formgo_list)
    

    sum_formdata = Form(
        **{column: sum(getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in formdata_list)
            for column in columns}
    )
    sum_formdata_go = Form_G_O(
        **{column: sum(getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in formgo_list)
            for column in columnsgo}
    )

    sum_formdata.labour_average_income_family = sum_formdata.labour_average_income_family / count_form if count_form != 0 else 0
    sum_formdata.labour_household_size = sum_formdata.labour_household_size / count_form if count_form != 0 else 0
    sum_formdata.credit_average_total = sum_formdata.credit_average_total / count_form if count_form != 0 else 0
    
    sum_formdata_go.labour_average_income_family = int(sum_formdata_go.labour_average_income_family / count_form_go) if count_form_go != 0 else 0
    sum_formdata_go.labour_household_size = int(int(sum_formdata_go.labour_household_size / count_form_go)) if count_form_go != 0 else 0
    sum_formdata_go.credit_average_total = int(sum_formdata_go.credit_average_total / count_form_go) if count_form_go != 0 else 0

    sum_formdata.credit_zalog = sum_formdata.credit_zalog / count_form if count_form != 0 else 0
    sum_formdata_go.credit_zalog = round(sum_formdata_go.credit_zalog / count_form_go, 2) if count_form_go != 0 else 0
    form = FormDataForm(obj=sum_formdata)
    
    if request.method == 'POST':
        if filterform.validate_on_submit():
            formdata_list = Form.query.filter(Form.kato_6.startswith(filterform.kato_4.data)).all()
            formgo_list = Form_G_O.query.filter(Form_G_O.kato_6.startswith(filterform.kato_4.data)).all()
            count_form = len(formdata_list)
            count_form_go = len(formgo_list)
            sum_formdata = Form(
                **{column: sum(getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in formdata_list)
                    for column in columns}
            )
            sum_formdata_go = Form_G_O(
                **{column: sum(getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in formgo_list)
                    for column in columnsgo}
            )
            sum_formdata.labour_average_income_family = sum_formdata.labour_average_income_family / count_form if count_form != 0 else 0
            sum_formdata.labour_household_size = sum_formdata.labour_household_size / count_form if count_form != 0 else 0
            sum_formdata.credit_average_total = sum_formdata.credit_average_total / count_form if count_form != 0 else 0
            
            sum_formdata_go.labour_average_income_family = int(sum_formdata_go.labour_average_income_family / count_form_go) if count_form_go != 0 else 0
            sum_formdata_go.labour_household_size = int(int(sum_formdata_go.labour_household_size / count_form_go)) if count_form_go != 0 else 0
            sum_formdata_go.credit_average_total = int(sum_formdata_go.credit_average_total / count_form_go) if count_form_go != 0 else 0

            sum_formdata.credit_zalog = sum_formdata.credit_zalog / count_form if count_form != 0 else 0
            sum_formdata_go.credit_zalog = round(sum_formdata_go.credit_zalog / count_form_go, 2) if count_form_go != 0 else 0
            form = FormDataForm(obj=sum_formdata)

            return render_template('region_akim.html', str=str, form=form, formGO=sum_formdata_go, user=current_user,
                               measurement_units=measurement_units, formdata=formdata_list, filterform=filterform)
        else:
            flash(f'Возникла ошибка: {filterform.errors}', 'error')
    return render_template('region_akim.html', str=str, form=form, formGO=sum_formdata_go, user=current_user,
                               measurement_units=measurement_units, formdata=formdata_list,filterform=filterform)
    

@app.route('/add-creditors', methods=['POST', 'GET'])
@login_required
def add_creditors():
    form = CreditorForm()
    if request.method == 'GET':
        return render_template('creditors.html', form=form, user=current_user, measurement_units=measurement_units)
    else:
        if form.validate_on_submit():
            creditor = Creditor(
                user_id = current_user.id,
                kato_2= current_user.kato_2,
                kato_2_name = current_user.kato_2_name,
                kato_4 = current_user.kato_4,
                kato_4_name = current_user.kato_4_name,
                kato_6 = current_user.kato_6,
                kato_6_name = current_user.kato_6_name,
                FIO = form.FIO.data,
                IIN = form.IIN.data,
                gender = form.gender.data,
                family_income_month = form.family_income_month.data,
                credit_goal = form.credit_goal.data,
                credit_other_goal = form.credit_other_goal.data,
                credit_amount = form.credit_amount.data,
                credit_period = form.credit_period.data,
                zalog_avaliability = form.zalog_avaliability.data,
                zalog_name = form.zalog_name.data,
                zalog_address = form.zalog_address.data,
                zalog_square = form.zalog_square.data,
                zalog_creation_year = form.zalog_creation_year.data,
                zalog_wall_material = form.zalog_wall_material.data,
                zalog_hoz_buildings = form.zalog_hoz_buildings.data,
                creditor_phone = form.creditor_phone.data
            )
            db.session.add(creditor)
            db.session.commit()
            flash("Заемщик успешно добавлен!", category='success')
            return redirect(url_for('all_creditors'))
        else:
            print(form.errors.items())
            flash('Заемщик не добавлен! Некорректные данные.', category='error')
    return render_template('creditors.html', form=form, user=current_user, measurement_units=measurement_units)
        
@app.route('/all-creditors', methods=['GET'])
@login_required
def all_creditors():
    form = CreditorForm()
    creditors = Creditor.query.filter_by(user_id=current_user.id).all()
    return render_template('all_creditors.html', form=form, creditors=creditors, measurement_units=measurement_units, user=current_user)

@app.route('/dashboard_soc1', methods=['GET'])
@login_required
def dashboard_soc1():

    formData=Form.query.filter_by(user_id=current_user.id).first()
    
    if current_user.is_district:
        return redirect(url_for('dashboard_all'))
    else:
        if not formData:
            flash('Отсутствует анкета', 'info')
            return redirect(url_for('login'))

    return render_template('dashboard_social_pocazat.html', round=round, formData=formData, user=current_user)

@app.route('/dashboard_animal', methods=['GET'])
@login_required
def dashboard_animal():
    formData=Form.query.filter_by(user_id=current_user.id).first()
    formRegion = Form.query.filter_by(kato_4 = current_user.kato_4).all()
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
    return render_template('animal_dashboard.html',factors_total=factors_total, round=round, formData=formData, user=current_user)

@app.route('/dashboard_plants', methods=['GET'])
@login_required
def dashboard_plants():
    formData=Form.query.filter_by(user_id=current_user.id).first()
    formRegion = Form.query.filter_by(kato_4 = current_user.kato_4).all()
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
    w_min = min(formData.dx_tomato, formData.dx_potato, formData.dx_cucumber, formData.dx_carrot, formData.dx_kapusta, formData.dx_svekla, formData.dx_onion, formData.dx_sweet_peper, formData.dx_chesnok, formData.dx_kabachek, formData.dx_fruits, formData.dx_korm)
    w_max = max(formData.dx_tomato, formData.dx_potato, formData.dx_cucumber, formData.dx_carrot, formData.dx_kapusta, formData.dx_svekla, formData.dx_onion, formData.dx_sweet_peper, formData.dx_chesnok, formData.dx_kabachek, formData.dx_fruits, formData.dx_korm)
    f1w1 = ((float((formData.dx_tomato - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w2 = ((float((formData.dx_cucumber - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w3 = ((float((formData.dx_potato - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w4 = ((float((formData.dx_carrot - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w5 = ((float((formData.dx_kapusta - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w6 = ((float((formData.dx_svekla - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w7 = ((float((formData.dx_onion - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w8 = ((float((formData.dx_sweet_peper - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w9 = ((float((formData.dx_chesnok - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w10 = ((float((formData.dx_kabachek - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w11 = ((float((formData.dx_fruits - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1w12 = ((float((formData.dx_korm - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
    f1_average = statistics.mean([f1w1, f1w2, f1w3, f1w4, f1w5, f1w6, f1w7, f1w8, f1w9, f1w10, f1w11, f1w12])

    f2_w_min = min(formData.dx_pashnya, formData.dx_mnogoletnie, formData.dx_zelej, formData.dx_pastbishe, formData.dx_senokosy, formData.dx_ogorody, formData.dx_sad)
    f2_w_max = max(formData.dx_pashnya, formData.dx_mnogoletnie, formData.dx_zelej, formData.dx_pastbishe, formData.dx_senokosy, formData.dx_ogorody, formData.dx_sad)
    f2w1 = ((float((formData.dx_pashnya - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w2 = ((float((formData.dx_mnogoletnie - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w3 = ((float((formData.dx_zelej - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w4 = ((float((formData.dx_pastbishe - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w5 = ((float((formData.dx_senokosy - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w6 = ((float((formData.dx_ogorody - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2w7 = ((float((formData.dx_sad - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
    f2_average = statistics.mean([f2w1, f2w2, f2w3, f2w4, f2w5, f2w6, f2w7])

    f3_w_min = min(formData.labour_private_ogorod, formData.labour_unemployed, formData.labour_total_econ_inactive_population)
    f3_w_max = max(formData.labour_private_ogorod, formData.labour_unemployed, formData.labour_total_econ_inactive_population)
    f3w1 = ((float((formData.labour_private_ogorod - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.2 if f3_w_max - f3_w_min > 0 else 0
    f3w2 = ((float((formData.labour_unemployed - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.2 if f3_w_max - f3_w_min > 0 else 0
    f3w3 = ((float((formData.labour_total_econ_inactive_population - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.2 if f3_w_max - f3_w_min > 0 else 0
    f3_average = statistics.mean([f3w1, f3w2, f3w3])

    f4w1 = formData.infrastructure_mtm * 0.2
    f4w2 = formData.infrastructure_slad * 0.2
    f4w3 = formData.infrastructure_garage * 0.2
    f4w4 = formData.infrastructure_cycsterny * 0.2
    f4w5 = formData.infrastructure_transformator * 0.2
    f4w6 = formData.infrastructure_polivochnaya_sistema_ * 0.2
    f4_average = statistics.mean([f4w1, f4w2, f4w3, f4w4, f4w5, f4w6])

    f6w1 = float((formData.labour_average_income_family / 120000)) * 0.15 
    f6w2 = float(formData.credit_amount / (credit_average_total_all / credit_amount_average_all)) * 0.15 if credit_amount_average_all > 0 else 0
    f6w3 = float(formData.credit_total / credit_total_all) * 0.15 if credit_total_all > 0 else 0
    f6w4 = float(formData.credit_average_total / credit_average_total_all) * 0.15 if credit_average_total_all > 0 else 0
    f6w5 = float(formData.credit_zalog)
    f6_average = statistics.mean([f6w1, f6w2, f6w3, f6w4, f6w5])

    factors_total = round(f1_average + f2_average + f3_average + f4_average + f6_average, 2)
    return render_template('plants_dashboard.html',factors_total=factors_total, round=round, formData=formData, user=current_user)

@app.route('/dashboard_business', methods=['GET'])
@login_required
def dashboard_business():

    formData=Form.query.filter_by(user_id=current_user.id).first()
    return render_template('business_dashboard.html', round=round, formData=formData, user=current_user)

@app.route('/dashboard_recycling', methods=['GET'])
@login_required
def dashboard_recycling():

    formData=Form.query.filter_by(user_id=current_user.id).first()
    return render_template('recycling_dashboard.html', round=round, formData=formData, user=current_user)

@app.route('/dashboard_credits', methods=['GET'])
@login_required
def dashboard_credits():

    formData=Form.query.filter_by(user_id=current_user.id).first()
    return render_template('credits_dashboard.html', round=round, formData=formData, user=current_user)

@app.route('/dashboard_plants_all', methods=['GET', 'POST'])
@login_required
def dashboard_plants_all():
    filterform = FilterForm()
    filterform.set_filter_choices(current_user.kato_4)
    formdata_list = Form.query.filter_by(kato_4=current_user.kato_4).all()
    count_form = len(formdata_list)
    inspector1 = inspect(Form)
    columns = inspector1.columns.keys()
    
    sum_formdata = Form(
        **{column: sum(getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in formdata_list)
            for column in columns}
    )

    credit_amount_average_all = sum_formdata.credit_amount
    credit_average_total_all = sum_formdata.credit_average_total
    credit_total_all = sum_formdata.credit_total
    credit_average_total_all = sum_formdata.credit_average_total / count_form
    if request.method == 'GET':
        return render_template('plants_dashboard_all.html',check_filter_all=True, filterform=filterform,round=round, formData=sum_formdata, user=current_user, form=formdata_list)
    else:
        if filterform.validate_on_submit():
            formdata_list = Form.query.filter(Form.kato_6.startswith(filterform.kato_4.data)).all()
            inspector1 = inspect(Form)
            columns = inspector1.columns.keys()
            check_filter_all = False
            if len(formdata_list)>1:
                check_filter_all = True
            sum_formdata = Form(
                **{column: sum(getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in formdata_list)
                    for column in columns}
            )
            w_min = min(sum_formdata.dx_tomato, sum_formdata.dx_potato, sum_formdata.dx_cucumber, sum_formdata.dx_carrot, sum_formdata.dx_kapusta, sum_formdata.dx_svekla, sum_formdata.dx_onion, sum_formdata.dx_sweet_peper, sum_formdata.dx_chesnok, sum_formdata.dx_kabachek, sum_formdata.dx_fruits, sum_formdata.dx_korm)
            w_max = max(sum_formdata.dx_tomato, sum_formdata.dx_potato, sum_formdata.dx_cucumber, sum_formdata.dx_carrot, sum_formdata.dx_kapusta, sum_formdata.dx_svekla, sum_formdata.dx_onion, sum_formdata.dx_sweet_peper, sum_formdata.dx_chesnok, sum_formdata.dx_kabachek, sum_formdata.dx_fruits, sum_formdata.dx_korm)
            f1w1 = ((float((sum_formdata.dx_tomato - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
            f1w2 = ((float((sum_formdata.dx_cucumber - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
            f1w3 = ((float((sum_formdata.dx_potato - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
            f1w4 = ((float((sum_formdata.dx_carrot - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
            f1w5 = ((float((sum_formdata.dx_kapusta - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
            f1w6 = ((float((sum_formdata.dx_svekla - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
            f1w7 = ((float((sum_formdata.dx_onion - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
            f1w8 = ((float((sum_formdata.dx_sweet_peper - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
            f1w9 = ((float((sum_formdata.dx_chesnok - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
            f1w10 = ((float((sum_formdata.dx_kabachek - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
            f1w11 = ((float((sum_formdata.dx_fruits - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
            f1w12 = ((float((sum_formdata.dx_korm - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
            f1_average = statistics.mean([f1w1, f1w2, f1w3, f1w4, f1w5, f1w6, f1w7, f1w8, f1w9, f1w10, f1w11, f1w12])

            f2_w_min = min(sum_formdata.dx_pashnya, sum_formdata.dx_mnogoletnie, sum_formdata.dx_zelej, sum_formdata.dx_pastbishe, sum_formdata.dx_senokosy, sum_formdata.dx_ogorody, sum_formdata.dx_sad)
            f2_w_max = max(sum_formdata.dx_pashnya, sum_formdata.dx_mnogoletnie, sum_formdata.dx_zelej, sum_formdata.dx_pastbishe, sum_formdata.dx_senokosy, sum_formdata.dx_ogorody, sum_formdata.dx_sad)
            f2w1 = ((float((sum_formdata.dx_pashnya - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
            f2w2 = ((float((sum_formdata.dx_mnogoletnie - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
            f2w3 = ((float((sum_formdata.dx_zelej - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
            f2w4 = ((float((sum_formdata.dx_pastbishe - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
            f2w5 = ((float((sum_formdata.dx_senokosy - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
            f2w6 = ((float((sum_formdata.dx_ogorody - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
            f2w7 = ((float((sum_formdata.dx_sad - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
            f2_average = statistics.mean([f2w1, f2w2, f2w3, f2w4, f2w5, f2w6, f2w7])

            f3_w_min = min(sum_formdata.labour_private_ogorod, sum_formdata.labour_unemployed, sum_formdata.labour_total_econ_inactive_population)
            f3_w_max = max(sum_formdata.labour_private_ogorod, sum_formdata.labour_unemployed, sum_formdata.labour_total_econ_inactive_population)
            f3w1 = ((float((sum_formdata.labour_private_ogorod - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.2 if f3_w_max - f3_w_min > 0 else 0
            f3w2 = ((float((sum_formdata.labour_unemployed - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.2 if f3_w_max - f3_w_min > 0 else 0
            f3w3 = ((float((sum_formdata.labour_total_econ_inactive_population - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.2 if f3_w_max - f3_w_min > 0 else 0
            f3_average = statistics.mean([f3w1, f3w2, f3w3])

            f4w1 = sum_formdata.infrastructure_mtm * 0.2
            f4w2 = sum_formdata.infrastructure_slad * 0.2
            f4w3 = sum_formdata.infrastructure_garage * 0.2
            f4w4 = sum_formdata.infrastructure_cycsterny * 0.2
            f4w5 = sum_formdata.infrastructure_transformator * 0.2
            f4w6 = sum_formdata.infrastructure_polivochnaya_sistema_ * 0.2
            f4_average = statistics.mean([f4w1, f4w2, f4w3, f4w4, f4w5, f4w6])

            f6w1 = float((sum_formdata.labour_average_income_family / 120000)) * 0.15 
            f6w2 = float(sum_formdata.credit_amount / (credit_average_total_all / credit_amount_average_all)) * 0.15 if credit_amount_average_all > 0 else 0
            f6w3 = float(sum_formdata.credit_total / credit_total_all) * 0.15 if credit_total_all > 0 else 0
            f6w4 = float(sum_formdata.credit_average_total / credit_average_total_all) * 0.15 if credit_average_total_all > 0 else 0
            f6w5 = float(sum_formdata.credit_zalog)
            f6_average = statistics.mean([f6w1, f6w2, f6w3, f6w4, f6w5])

            factors_total = round(f1_average + f2_average + f3_average + f4_average + f6_average, 2)
        else:
            flash(f'Возникла ошибка: {filterform.errors}', category='error')
            formdata_list = Form.query.filter_by(kato_4=current_user.kato_4).all()
            count_form = len(formdata_list)
            inspector1 = inspect(Form)
            columns = inspector1.columns.keys()

            sum_formdata = Form(
                **{column: sum(getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in formdata_list)
                    for column in columns}
            )
            return render_template('plants_dashboard_all.html',factors_total=factors_total, check_filter_all=check_filter_all,filterform=filterform,round=round, formData=sum_formdata, user=current_user)

    return render_template('plants_dashboard_all.html',factors_total=factors_total,check_filter_all=check_filter_all, filterform=filterform,round=round, formData=sum_formdata, user=current_user)

@app.route('/dashboard_animals_all', methods=['GET', 'POST'])
@login_required
def dashboard_animals_all():
    filterform = FilterForm()
    filterform.set_filter_choices(current_user.kato_4)
    formdata_list = Form.query.filter_by(kato_4=current_user.kato_4).all()
    count_form = len(formdata_list)
    inspector1 = inspect(Form)
    columns = inspector1.columns.keys()

    sum_formdata = Form(
        **{column: sum(getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in formdata_list)
            for column in columns}
    )
    credit_amount_average_all = sum_formdata.credit_amount
    credit_average_total_all = sum_formdata.credit_average_total
    credit_total_all = sum_formdata.credit_total
    credit_average_total_all = sum_formdata.credit_average_total / count_form
    if request.method == 'GET':
        
        return render_template('animal_dashboard_all.html',check_filter_all=True, filterform=filterform,round=round, formData=sum_formdata, user=current_user, form=formdata_list)
    else:
        if filterform.validate_on_submit():
            formdata_list = Form.query.filter(Form.kato_6.startswith(filterform.kato_4.data)).all()
            inspector1 = inspect(Form)
            columns = inspector1.columns.keys()
            check_filter_all = False
            if len(formdata_list)>1:
                check_filter_all = True

            sum_formdata = Form(
                **{column: sum(getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in formdata_list)
                    for column in columns}
            )
            w_min = min(sum_formdata.animal_krs_milk, sum_formdata.animal_krs_meat, sum_formdata.animal_sheep, sum_formdata.animal_kozel, sum_formdata.animal_horse, sum_formdata.animal_chicken, sum_formdata.animal_gusi, sum_formdata.animal_duck, sum_formdata.animal_induk)
            w_max = max(sum_formdata.animal_krs_milk, sum_formdata.animal_krs_meat, sum_formdata.animal_sheep, sum_formdata.animal_kozel, sum_formdata.animal_horse, sum_formdata.animal_chicken, sum_formdata.animal_gusi, sum_formdata.animal_duck, sum_formdata.animal_induk)
            f1w1 = ((float((sum_formdata.animal_krs_milk - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
            f1w2 = ((float((sum_formdata.animal_krs_meat - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
            f1w3 = ((float((sum_formdata.animal_sheep - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
            f1w4 = ((float((sum_formdata.animal_kozel - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
            f1w5 = ((float((sum_formdata.animal_horse - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
            f1w6 = ((float((sum_formdata.animal_chicken - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
            f1w7 = ((float((sum_formdata.animal_gusi - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
            f1w8 = ((float((sum_formdata.animal_duck - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
            f1w9 = ((float((sum_formdata.animal_induk - w_min) / (w_max - w_min))) * 100) * 0.15 if w_max - w_min > 0 else 0
            f1_average = statistics.mean([f1w1, f1w2, f1w3, f1w4, f1w5, f1w6, f1w7, f1w8, f1w9])

            eggs_tonn = (sum_formdata.animal_egg_chicken * 60) / 1000000
            f2_w_min = min(sum_formdata.animal_meat_cow, sum_formdata.animal_meat_sheep, sum_formdata.animal_meat_horse, sum_formdata.animal_meat_chicken, sum_formdata.animal_milk_cow, sum_formdata.animal_mil_kozel, sum_formdata.animal_milk_horse, Decimal(eggs_tonn))
            f2_w_max = max(sum_formdata.animal_meat_cow, sum_formdata.animal_meat_sheep, sum_formdata.animal_meat_horse, sum_formdata.animal_meat_chicken, sum_formdata.animal_milk_cow, sum_formdata.animal_mil_kozel, sum_formdata.animal_milk_horse, Decimal(eggs_tonn))
            f2w1 = ((float((sum_formdata.animal_meat_cow - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
            f2w2 = ((float((sum_formdata.animal_meat_sheep - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
            f2w3 = ((float((sum_formdata.animal_meat_horse - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
            f2w4 = ((float((sum_formdata.animal_meat_chicken - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
            f2w5 = ((float((sum_formdata.animal_milk_cow - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
            f2w6 = ((float((sum_formdata.animal_mil_kozel - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
            f2w7 = ((float((sum_formdata.animal_milk_horse - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
            f2w8 = ((float((Decimal(eggs_tonn) - f2_w_min) / (f2_w_max - f2_w_min))) * 100) * 0.15 if f2_w_max - f2_w_min > 0 else 0
            f2_average = statistics.mean([f2w1, f2w2, f2w3, f2w4, f2w5, f2w6, f2w7, f2w8])

            f3_w_min = min(sum_formdata.animal_pashnya, sum_formdata.animal_mnogolet, sum_formdata.animal_zalej, sum_formdata.animal_pastbisha, sum_formdata.animal_senokos, sum_formdata.animal_ogorod, sum_formdata.animal_sad)
            f3_w_max = max(sum_formdata.animal_pashnya, sum_formdata.animal_mnogolet, sum_formdata.animal_zalej, sum_formdata.animal_pastbisha, sum_formdata.animal_senokos, sum_formdata.animal_ogorod, sum_formdata.animal_sad)
            f3w1 = ((float((sum_formdata.animal_pashnya - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.1 if f3_w_max - f3_w_min > 0 else 0
            f3w2 = ((float((sum_formdata.animal_mnogolet - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.1 if f3_w_max - f3_w_min > 0 else 0
            f3w3 = ((float((sum_formdata.animal_zalej - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.1 if f3_w_max - f3_w_min > 0 else 0
            f3w4 = ((float((sum_formdata.animal_pastbisha - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.1 if f3_w_max - f3_w_min > 0 else 0
            f3w5 = ((float((sum_formdata.animal_senokos - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.1 if f3_w_max - f3_w_min > 0 else 0
            f3w6 = ((float((sum_formdata.animal_ogorod - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.1 if f3_w_max - f3_w_min > 0 else 0
            f3w7 = ((float((sum_formdata.animal_sad - f3_w_min) / (f3_w_max - f3_w_min))) * 100) * 0.1 if f3_w_max - f3_w_min > 0 else 0
            f3_average = statistics.mean([f3w1, f3w2, f3w3, f3w4, f3w5, f3w6, f3w7])

            f4_w_min = min(sum_formdata.labour_private_ogorod, sum_formdata.labour_unemployed, sum_formdata.labour_total_econ_inactive_population)
            f4_w_max = max(sum_formdata.labour_private_ogorod, sum_formdata.labour_unemployed, sum_formdata.labour_total_econ_inactive_population)
            f4w1 = ((float((sum_formdata.labour_private_ogorod - f4_w_min) / (f4_w_max - f4_w_min))) * 100) * 0.2 if f4_w_max - f4_w_min > 0 else 0
            f4w2 = ((float((sum_formdata.labour_unemployed - f4_w_min) / (f4_w_max - f4_w_min))) * 100) * 0.2 if f4_w_max - f4_w_min > 0 else 0
            f4w3 = ((float((sum_formdata.labour_total_econ_inactive_population - f4_w_min) / (f4_w_max - f4_w_min))) * 100) * 0.2 if f4_w_max - f4_w_min > 0 else 0
            f4_average = statistics.mean([f4w1, f4w2, f4w3])

            f5w1 = sum_formdata.infrastructure_mtm * 0.15
            f5w2 = sum_formdata.infrastructure_slad * 0.15
            f5w3 = sum_formdata.infrastructure_garage * 0.15
            f5w4 = sum_formdata.infrastructure_cycsterny * 0.15
            f5w5 = sum_formdata.infrastructure_transformator * 0.15
            f5w6 = sum_formdata.infrastructure_polivochnaya_sistema_ * 0.15
            f5_average = statistics.mean([f5w1, f5w2, f5w3, f5w4, f5w5, f5w6])

            f7w1 = float((sum_formdata.labour_average_income_family / 120000)) * 0.15 
            f7w2 = float(sum_formdata.credit_amount / (credit_average_total_all / credit_amount_average_all)) * 0.15 if credit_amount_average_all > 0 else 0
            f7w3 = float(sum_formdata.credit_total / credit_total_all) * 0.15 if credit_total_all > 0 else 0
            f7w4 = float(sum_formdata.credit_average_total / credit_average_total_all) * 0.15 if credit_average_total_all > 0 else 0
            f7w5 = float(sum_formdata.credit_zalog)
            f7_average = statistics.mean([f7w1, f7w2, f7w3, f7w4, f7w5])
            factors_total = round(f1_average + f2_average + f3_average + f4_average + f5_average + f7_average, 2)
        else:
            flash(f'Возникла ошибка: {filterform.errors}', category='error')
            formdata_list = Form.query.filter_by(kato_4=current_user.kato_4).all()
            inspector1 = inspect(Form)
            columns = inspector1.columns.keys()

            sum_formdata = Form(
                **{column: sum(getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in formdata_list)
                    for column in columns}
            )
            return render_template('animal_dashboard_all.html',factors_total=factors_total,check_filter_all=check_filter_all, filterform=filterform,round=round, formData=sum_formdata, user=current_user, form=formdata_list)
    
    return render_template('animal_dashboard_all.html',factors_total=factors_total,check_filter_all=check_filter_all, filterform=filterform,round=round, formData=sum_formdata, user=current_user)


@app.route('/dashboard_business_all', methods=['GET', 'POST'])
@login_required
def dashboard_business_all():
    filterform = FilterForm()
    filterform.set_filter_choices(current_user.kato_4)
    if request.method == 'GET':
        formdata_list = Form.query.filter_by(kato_4=current_user.kato_4).all()
        count_form = len(formdata_list)
        inspector1 = inspect(Form)
        columns = inspector1.columns.keys()

        sum_formdata = Form(
            **{column: sum(
                getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in
                formdata_list)
               for column in columns}
        )
        sum_formdata.infrastructure_polivy = round(sum_formdata.infrastructure_polivy / count_form, 2) if count_form != 0 else 0

        return render_template('dashboard_business_all.html', filterform=filterform, round=round, formData=sum_formdata,
                               user=current_user, form=formdata_list)
    else:
        if filterform.validate_on_submit():
            formdata_list = Form.query.filter(Form.kato_6.startswith(filterform.kato_4.data)).all()
            inspector1 = inspect(Form)
            columns = inspector1.columns.keys()

            sum_formdata = Form(
                **{column: sum(
                    getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in
                    formdata_list)
                   for column in columns}
            )
        else:
            flash(f'Возникла ошибка: {filterform.errors}', category='error')
            formdata_list = Form.query.filter_by(kato_4=current_user.kato_4).all()
            inspector1 = inspect(Form)
            columns = inspector1.columns.keys()

            sum_formdata = Form(
                **{column: sum(
                    getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in
                    formdata_list)
                   for column in columns}
            )
            return render_template('dashboard_business_all.html', filterform=filterform, round=round,
                                   formData=sum_formdata, user=current_user, form=formdata_list)

    return render_template('dashboard_business_all.html', filterform=filterform, round=round, formData=sum_formdata,
                           user=current_user)

@app.route('/dashboard_recycling_all', methods=['GET', 'POST'])
@login_required
def dashboard_recycling_all():
    filterform = FilterForm()
    filterform.set_filter_choices(current_user.kato_4)
    if request.method == 'GET':
        formdata_list = Form.query.filter_by(kato_4=current_user.kato_4).all()
        count_form = len(formdata_list)
        inspector1 = inspect(Form)
        columns = inspector1.columns.keys()

        sum_formdata = Form(
            **{column: sum(
                getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in
                formdata_list)
               for column in columns}
        )
        return render_template('recycling_dashboard_all.html', filterform=filterform, round=round, formData=sum_formdata,
                               user=current_user, form=formdata_list)
    else:
        if filterform.validate_on_submit():
            formdata_list = Form.query.filter(Form.kato_6.startswith(filterform.kato_4.data)).all()
            inspector1 = inspect(Form)
            columns = inspector1.columns.keys()

            sum_formdata = Form(
                **{column: sum(
                    getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in
                    formdata_list)
                   for column in columns}
            )
        else:
            flash(f'Возникла ошибка: {filterform.errors}', category='error')
            formdata_list = Form.query.filter_by(kato_4=current_user.kato_4).all()
            inspector1 = inspect(Form)
            columns = inspector1.columns.keys()

            sum_formdata = Form(
                **{column: sum(
                    getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in
                    formdata_list)
                   for column in columns}
            )
            return render_template('recycling_dashboard_all.html', filterform=filterform, round=round,
                                   formData=sum_formdata, user=current_user, form=formdata_list)

    return render_template('recycling_dashboard_all.html', filterform=filterform, round=round, formData=sum_formdata,
                           user=current_user)

@app.route('/dashboard_credits_all', methods=['GET', 'POST'])
@login_required
def dashboard_credits_all():
    filterform = FilterForm()
    filterform.set_filter_choices(current_user.kato_4)
    if request.method == 'GET':
        formdata_list = Form.query.filter_by(kato_4=current_user.kato_4).all()
        count_form = len(formdata_list)
        inspector1 = inspect(Form)
        columns = inspector1.columns.keys()

        sum_formdata = Form(
            **{column: sum(
                getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in
                formdata_list)
               for column in columns}
        )
        sum_formdata.credit_average_total = int(sum_formdata.credit_average_total / count_form) if count_form != 0 else 0
        sum_formdata.credit_zalog = round(sum_formdata.credit_zalog / count_form, 2) if count_form != 0 else 0

        return render_template('credits_dashboard_all.html', filterform=filterform, round=round, formData=sum_formdata,
                               user=current_user, form=formdata_list)
    else:
        if filterform.validate_on_submit():
            formdata_list = Form.query.filter(Form.kato_6.startswith(filterform.kato_4.data)).all()
            inspector1 = inspect(Form)
            columns = inspector1.columns.keys()
            count_form = len(formdata_list)

            sum_formdata = Form(
                **{column: sum(
                    getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in
                    formdata_list)
                   for column in columns}
            )
            sum_formdata.credit_average_total = int(sum_formdata.credit_average_total / count_form) if count_form != 0 else 0
            sum_formdata.credit_zalog = round(sum_formdata.credit_zalog / count_form, 2) if count_form != 0 else 0

        else:
            flash(f'Возникла ошибка: {filterform.errors}', category='error')
            formdata_list = Form.query.filter_by(kato_4=current_user.kato_4).all()
            inspector1 = inspect(Form)
            columns = inspector1.columns.keys()
            count_form = len(formdata_list)

            sum_formdata = Form(
                **{column: sum(
                    getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in
                    formdata_list)
                   for column in columns}
            )
            sum_formdata.credit_average_total = int(sum_formdata.credit_average_total / count_form) if count_form != 0 else 0
            sum_formdata.credit_zalog = round(sum_formdata.credit_zalog / count_form, 2) if count_form != 0 else 0

            return render_template('credits_dashboard_all.html', filterform=filterform, round=round,
                                   formData=sum_formdata, user=current_user, form=formdata_list)

    return render_template('credits_dashboard_all.html', filterform=filterform, round=round, formData=sum_formdata,
                           user=current_user)


@app.route('/dashboard_all', methods=['GET', 'POST'])
@login_required
def dashboard_all():
    filterform = FilterForm()
    filterform.set_filter_choices(current_user.kato_4)
    if request.method == 'GET':
        formdata = Form.query.filter_by(kato_4=current_user.kato_4).all()
        if not formdata:
            flash('Отсутствуют анкеты', 'info')
            return redirect(url_for('login'))
        counter = 0
        labour_labour_total = 0
        labour_population_total = 0
        labour_active_total = 0
        labour_inactive_total = 0
        labour_private_ogorod_total = 0
        house_total_dvor_total = 0
        house_zaselen_dvor_total = 0
        labour_employed_precent = 0
        labour_unemployed_precent = 0
        labour_average_income_family_total = 0
        labour_household_size_total = 0
        labour_constant_population_total = 0
        labour_government_workers_total = 0
        labour_private_labour_total = 0
        labour_total_econ_inactive_population_total = 0
        labour_unemployed_total = 0
        dx_cx_land_total = 0
        dx_pashnya_total = 0
        dx_mnogoletnie_total = 0
        dx_zelej_total = 0
        dx_pastbishe_total = 0
        dx_senokosy_total = 0
        dx_ogorody_total = 0
        dx_sad_total = 0
        for form in formdata:
            counter += 1
            labour_total_econ_inactive_population_total += form.labour_total_econ_inactive_population
            labour_unemployed_total += form.labour_unemployed
            labour_private_labour_total += form.labour_private_labour
            labour_government_workers_total += form.labour_government_workers
            labour_labour_total += form.labour_labour
            labour_constant_population_total += form.labour_constant_population
            labour_population_total += form.labour_population
            labour_active_total += (form.labour_government_workers + form.labour_private_labour + form.labour_private_ogorod)
            labour_inactive_total += (form.labour_unemployed + form.labour_total_econ_inactive_population)
            labour_average_income_family_total += form.labour_average_income_family
            labour_private_ogorod_total += form.labour_private_ogorod
            labour_household_size_total += form.labour_household_size
            house_total_dvor_total += form.house_total_dvor
            house_zaselen_dvor_total += form.house_zaselen_dvor
            dx_cx_land_total += form.dx_cx_land
            dx_pashnya_total += form.dx_pashnya
            dx_mnogoletnie_total += form.dx_mnogoletnie
            dx_zelej_total += form.dx_zelej
            dx_pastbishe_total += form.dx_pastbishe
            dx_senokosy_total += form.dx_senokosy
            dx_ogorody_total += form.dx_ogorody
            dx_sad_total += form.dx_sad

        
        labour_household_size_total_average = round(house_total_dvor_total / counter, 2) if counter != 0 else 0
        labour_average_income_family_total_average = round(labour_average_income_family_total / counter, 2) if counter != 0 else 0
        if int(labour_population_total) != 0:
            labour_employed_precent += round((int(labour_active_total) * 100) / int(labour_population_total), 2)
        else:
            labour_employed_precent = 0  # or set it to some default value

        if int(labour_population_total) != 0:
            labour_unemployed_precent += round((int(labour_inactive_total) * 100) / int(labour_population_total), 2)
        else:
            labour_unemployed_precent = 0 

        dashboard_all_data = {
            'labour_total_econ_inactive_population_total':labour_total_econ_inactive_population_total,
            'labour_unemployed_total':labour_unemployed_total,
            'labour_private_labour_total': labour_private_labour_total,
            'labour_government_workers_total':labour_government_workers_total,
            'labour_labour_total':labour_labour_total,
            'labour_constant_population_total': labour_constant_population_total,
            'labour_population_total': labour_population_total,
            'labour_active_total': labour_active_total,
            'labour_inactive_total': labour_inactive_total,
            'labour_private_ogorod_total': labour_private_ogorod_total,
            'house_total_dvor_total': house_total_dvor_total,
            'house_zaselen_dvor_total': house_zaselen_dvor_total,
            'labour_employed_precent': labour_employed_precent,
            'labour_unemployed_precent': labour_unemployed_precent,
            'labour_household_size_total_average': labour_household_size_total_average,
            'labour_average_income_family_total_average': labour_average_income_family_total_average,
            'dx_cx_land_total': dx_cx_land_total,
            'dx_pashnya_total': dx_pashnya_total,
            'dx_mnogoletnie_total': dx_mnogoletnie_total,
            'dx_zelej_total': dx_zelej_total,
            'dx_pastbishe_total': dx_pastbishe_total,
            'dx_senokosy_total': dx_senokosy_total,
            'dx_ogorody_total': dx_ogorody_total,
            'dx_sad_total': dx_sad_total
        }
        return render_template('dashboard_all.html',filterform = filterform,round=round, formData = formdata, user=current_user, dashboard_all_data=dashboard_all_data)
    else:
        if filterform.validate_on_submit():
            formdata = Form.query.filter(Form.kato_6.startswith(filterform.kato_4.data)).all()
            counter = 0
            labour_labour_total = 0
            labour_population_total = 0
            labour_active_total = 0
            labour_inactive_total = 0
            labour_private_ogorod_total = 0
            house_total_dvor_total = 0
            house_zaselen_dvor_total = 0
            labour_employed_precent = 0
            labour_unemployed_precent = 0
            labour_average_income_family_total = 0
            labour_household_size_total = 0
            labour_constant_population_total = 0
            labour_government_workers_total = 0
            labour_private_labour_total = 0
            labour_total_econ_inactive_population_total = 0
            labour_unemployed_total = 0
            dx_cx_land_total = 0
            dx_pashnya_total = 0
            dx_mnogoletnie_total = 0
            dx_zelej_total = 0
            dx_pastbishe_total = 0
            dx_senokosy_total = 0
            dx_ogorody_total = 0
            dx_sad_total = 0
            for form in formdata:
                counter += 1
                labour_total_econ_inactive_population_total += form.labour_total_econ_inactive_population
                labour_unemployed_total += form.labour_unemployed
                labour_private_labour_total += form.labour_private_labour
                labour_government_workers_total += form.labour_government_workers
                labour_labour_total += form.labour_labour
                labour_constant_population_total += form.labour_constant_population
                labour_population_total += form.labour_population
                labour_active_total += (form.labour_government_workers + form.labour_private_labour + form.labour_private_ogorod)
                labour_inactive_total += (form.labour_unemployed + form.labour_total_econ_inactive_population)
                labour_average_income_family_total += form.labour_average_income_family
                labour_private_ogorod_total += form.labour_private_ogorod
                labour_household_size_total += form.labour_household_size
                house_total_dvor_total += form.house_total_dvor
                house_zaselen_dvor_total += form.house_zaselen_dvor
                dx_cx_land_total += form.dx_cx_land
                dx_pashnya_total += form.dx_pashnya
                dx_mnogoletnie_total += form.dx_mnogoletnie
                dx_zelej_total += form.dx_zelej
                dx_pastbishe_total += form.dx_pastbishe
                dx_senokosy_total += form.dx_senokosy
                dx_ogorody_total += form.dx_ogorody
                dx_sad_total += form.dx_sad

            
            labour_household_size_total_average = round(house_total_dvor_total / counter, 2) if counter != 0 else 0
            labour_average_income_family_total_average = round(labour_average_income_family_total / counter, 2) if counter != 0 else 0
            if int(labour_population_total) != 0:
                labour_employed_precent += round((int(labour_active_total) * 100) / int(labour_population_total), 2)
            else:
                labour_employed_precent = 0  # or set it to some default value

            if int(labour_population_total) != 0:
                labour_unemployed_precent += round((int(labour_inactive_total) * 100) / int(labour_population_total), 2)
            else:
                labour_unemployed_precent = 0 


            dashboard_all_data = {
                'labour_total_econ_inactive_population_total':labour_total_econ_inactive_population_total,
                'labour_unemployed_total':labour_unemployed_total,
                'labour_private_labour_total': labour_private_labour_total,
                'labour_government_workers_total':labour_government_workers_total,
                'labour_labour_total':labour_labour_total,
                'labour_constant_population_total': labour_constant_population_total,
                'labour_population_total': labour_population_total,
                'labour_active_total': labour_active_total,
                'labour_inactive_total': labour_inactive_total,
                'labour_private_ogorod_total': labour_private_ogorod_total,
                'house_total_dvor_total': house_total_dvor_total,
                'house_zaselen_dvor_total': house_zaselen_dvor_total,
                'labour_employed_precent': labour_employed_precent,
                'labour_unemployed_precent': labour_unemployed_precent,
                'labour_household_size_total_average': labour_household_size_total_average,
                'labour_average_income_family_total_average': labour_average_income_family_total_average,
                'dx_cx_land_total': dx_cx_land_total,
                'dx_pashnya_total': dx_pashnya_total,
                'dx_mnogoletnie_total': dx_mnogoletnie_total,
                'dx_zelej_total': dx_zelej_total,
                'dx_pastbishe_total': dx_pastbishe_total,
                'dx_senokosy_total': dx_senokosy_total,
                'dx_ogorody_total': dx_ogorody_total,
                'dx_sad_total': dx_sad_total
            }
            return render_template('dashboard_all.html',filterform = filterform,round=round, formData = formdata, user=current_user, dashboard_all_data=dashboard_all_data)
        else:
            flash(f'Возникла ошибка: {filterform.errors}','error')
            formdata = Form.query.filter_by(kato_4=current_user.kato_4).all()
            counter = 0
            labour_labour_total = 0
            labour_population_total = 0
            labour_active_total = 0
            labour_inactive_total = 0
            labour_private_ogorod_total = 0
            house_total_dvor_total = 0
            house_zaselen_dvor_total = 0
            labour_employed_precent = 0
            labour_unemployed_precent = 0
            labour_average_income_family_total = 0
            labour_household_size_total = 0
            labour_constant_population_total = 0
            labour_government_workers_total = 0
            labour_private_labour_total = 0
            labour_total_econ_inactive_population_total = 0
            labour_unemployed_total = 0
            dx_cx_land_total = 0
            dx_pashnya_total = 0
            dx_mnogoletnie_total = 0
            dx_zelej_total = 0
            dx_pastbishe_total = 0
            dx_senokosy_total = 0
            dx_ogorody_total = 0
            dx_sad_total = 0
            for form in formdata:
                counter += 1
                labour_total_econ_inactive_population_total += form.labour_total_econ_inactive_population
                labour_unemployed_total += form.labour_unemployed
                labour_private_labour_total += form.labour_private_labour
                labour_government_workers_total += form.labour_government_workers
                labour_labour_total += form.labour_labour
                labour_constant_population_total += form.labour_constant_population
                labour_population_total += form.labour_population
                labour_active_total += (form.labour_government_workers + form.labour_private_labour + form.labour_private_ogorod)
                labour_inactive_total += (form.labour_unemployed + form.labour_total_econ_inactive_population)
                labour_average_income_family_total += form.labour_average_income_family
                labour_private_ogorod_total += form.labour_private_ogorod
                labour_household_size_total += form.labour_household_size
                house_total_dvor_total += form.house_total_dvor
                house_zaselen_dvor_total += form.house_zaselen_dvor
                dx_cx_land_total += form.dx_cx_land
                dx_pashnya_total += form.dx_pashnya
                dx_mnogoletnie_total += form.dx_mnogoletnie
                dx_zelej_total += form.dx_zelej
                dx_pastbishe_total += form.dx_pastbishe
                dx_senokosy_total += form.dx_senokosy
                dx_ogorody_total += form.dx_ogorody
                dx_sad_total += form.dx_sad

            
            labour_household_size_total_average = round(house_total_dvor_total / counter, 2) if counter != 0 else 0
            labour_average_income_family_total_average = round(labour_average_income_family_total / counter, 2) if counter != 0 else 0
            if int(labour_population_total) != 0:
                labour_employed_precent += round((int(labour_active_total) * 100) / int(labour_population_total), 2)
            else:
                labour_employed_precent = 0  # or set it to some default value

            if int(labour_population_total) != 0:
                labour_unemployed_precent += round((int(labour_inactive_total) * 100) / int(labour_population_total), 2)
            else:
                labour_unemployed_precent = 0 

            dashboard_all_data = {
                'labour_total_econ_inactive_population_total':labour_total_econ_inactive_population_total,
                'labour_unemployed_total':labour_unemployed_total,
                'labour_private_labour_total': labour_private_labour_total,
                'labour_government_workers_total':labour_government_workers_total,
                'labour_labour_total':labour_labour_total,
                'labour_constant_population_total': labour_constant_population_total,
                'labour_population_total': labour_population_total,
                'labour_active_total': labour_active_total,
                'labour_inactive_total': labour_inactive_total,
                'labour_private_ogorod_total': labour_private_ogorod_total,
                'house_total_dvor_total': house_total_dvor_total,
                'house_zaselen_dvor_total': house_zaselen_dvor_total,
                'labour_employed_precent': labour_employed_precent,
                'labour_unemployed_precent': labour_unemployed_precent,
                'labour_household_size_total_average': labour_household_size_total_average,
                'labour_average_income_family_total_average': labour_average_income_family_total_average,
                'dx_cx_land_total': dx_cx_land_total,
                'dx_pashnya_total': dx_pashnya_total,
                'dx_mnogoletnie_total': dx_mnogoletnie_total,
                'dx_zelej_total': dx_zelej_total,
                'dx_pastbishe_total': dx_pastbishe_total,
                'dx_senokosy_total': dx_senokosy_total,
                'dx_ogorody_total': dx_ogorody_total,
                'dx_sad_total': dx_sad_total
            }
            return render_template('dashboard_all.html',filterform = filterform,round=round, formData = formdata, user=current_user, dashboard_all_data=dashboard_all_data)
    return render_template('dashboard_all.html',round=round, formData = formdata, user=current_user, dashboard_all_data=dashboard_all_data)
    


@app.route('/form_village', methods=['POST', 'GET'])
@login_required
def form_village():
    user = current_user
    form = FormDataForm()
    form_check = Form.query.filter_by(user_id=current_user.id).first()
    if request.method == "GET":
        if form_check:
            flash("У вас уже имеется форма", category='info')
            return redirect(url_for('account'))
        else:
            return render_template('ms_form.html', form=form, measurement_units=measurement_units, user=user)
    else:
        if form_check:
            flash("У вас уже имеется форма", category='info')
            return redirect(url_for('account'))
        if form.validate_on_submit():
            excluded_fields = ['csrf_token', 'submit'] + [field.name for field in form if field.name.startswith('specialization_')]            
            form_data = {
                'user_id': current_user.id,
                'form_year': datetime.now().year,
                'kato_2': current_user.kato_2,
                'kato_2_name': current_user.kato_2_name,
                'kato_4': current_user.kato_4,
                'kato_4_name': current_user.kato_4_name,
                'kato_6': current_user.kato_6,
                'kato_6_name': current_user.kato_6_name,
                **{field.name: getattr(form, field.name).data for field in form if field.name not in excluded_fields}
            }
            spec_str_rast = ''
            for field in form:
                if field.name.startswith('specialization_rastenivodstvo_'):
                    if field.data == True:
                        spec_str_rast += str(field.label.text) + ', '
            spec_str_animal = ''
            for field in form:
                if field.name.startswith('specialization_animal_'):
                    if field.data == True:
                        spec_str_animal += str(field.label.text) + ', '
            form_data['specialization_animal'] = spec_str_animal[:-2]
            form_data['specialization_rastenivodstvo'] = spec_str_rast[:-2]
            formdata = Form(**form_data)
            db.session.add(formdata)
            db.session.commit()
            flash("Форма успешено добавлена!", 'success')
            return redirect(url_for('account'))
        else:
            print(form.errors)
            print(current_user)
            flash("Форма заполнена некорректно или отсутствуют необходимые поля.", 'error')
    return render_template('ms_form.html', title='Форма отчетности МСХ',form=form, measurement_units=measurement_units, user=current_user)
