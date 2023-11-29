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

    sum_formdata.labour_average_income_family = sum_formdata.labour_average_income_family / count_form if count_form != 0 else "Cannot divide by zero"
    sum_formdata.labour_household_size = sum_formdata.labour_household_size / count_form if count_form != 0 else "Cannot divide by zero"
    sum_formdata.credit_average_total = sum_formdata.credit_average_total / count_form if count_form != 0 else "Cannot divide by zero"
    
    sum_formdata_go.labour_average_income_family = int(sum_formdata_go.labour_average_income_family / count_form_go) if count_form_go != 0 else "Cannot divide by zero"
    sum_formdata_go.labour_household_size = int(int(sum_formdata_go.labour_household_size / count_form_go)) if count_form_go != 0 else "Cannot divide by zero"
    sum_formdata_go.credit_average_total = int(sum_formdata_go.credit_average_total / count_form_go) if count_form_go != 0 else "Cannot divide by zero"

    sum_formdata.credit_zalog = sum_formdata.credit_zalog / count_form if count_form != 0 else "Cannot divide by zero"
    sum_formdata_go.credit_zalog = round(sum_formdata_go.credit_zalog / count_form_go, 2) if count_form_go != 0 else "Cannot divide by zero"
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
            sum_formdata.labour_average_income_family = sum_formdata.labour_average_income_family / count_form if count_form != 0 else "Cannot divide by zero"
            sum_formdata.labour_household_size = sum_formdata.labour_household_size / count_form if count_form != 0 else "Cannot divide by zero"
            sum_formdata.credit_average_total = sum_formdata.credit_average_total / count_form if count_form != 0 else "Cannot divide by zero"
            
            sum_formdata_go.labour_average_income_family = int(sum_formdata_go.labour_average_income_family / count_form_go) if count_form_go != 0 else "Cannot divide by zero"
            sum_formdata_go.labour_household_size = int(int(sum_formdata_go.labour_household_size / count_form_go)) if count_form_go != 0 else "Cannot divide by zero"
            sum_formdata_go.credit_average_total = int(sum_formdata_go.credit_average_total / count_form_go) if count_form_go != 0 else "Cannot divide by zero"

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
    return render_template('animal_dashboard.html', round=round, formData=formData, user=current_user)

@app.route('/dashboard_plants', methods=['GET'])
@login_required
def dashboard_plants():

    formData=Form.query.filter_by(user_id=current_user.id).first()
    return render_template('plants_dashboard.html', round=round, formData=formData, user=current_user)

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
    if request.method == 'GET':
        formdata_list = Form.query.filter_by(kato_4=current_user.kato_4).all()
        count_form = len(formdata_list)
        inspector1 = inspect(Form)
        columns = inspector1.columns.keys()

        sum_formdata = Form(
            **{column: sum(getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in formdata_list)
                for column in columns}
        )

        return render_template('plants_dashboard_all.html', filterform=filterform,round=round, formData=sum_formdata, user=current_user, form=formdata_list)
    else:
        if filterform.validate_on_submit():
            formdata_list = Form.query.filter(Form.kato_6.startswith(filterform.kato_4.data)).all()
            inspector1 = inspect(Form)
            columns = inspector1.columns.keys()

            sum_formdata = Form(
                **{column: sum(getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in formdata_list)
                    for column in columns}
            )
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
            return render_template('plants_dashboard_all.html', filterform=filterform,round=round, formData=sum_formdata, user=current_user)

    return render_template('plants_dashboard_all.html', filterform=filterform,round=round, formData=sum_formdata, user=current_user)

@app.route('/dashboard_animals_all', methods=['GET', 'POST'])
@login_required
def dashboard_animals_all():
    filterform = FilterForm()
    filterform.set_filter_choices(current_user.kato_4)
    if request.method == 'GET':
        formdata_list = Form.query.filter_by(kato_4=current_user.kato_4).all()
        count_form = len(formdata_list)
        inspector1 = inspect(Form)
        columns = inspector1.columns.keys()

        sum_formdata = Form(
            **{column: sum(getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in formdata_list)
                for column in columns}
        )
        return render_template('animal_dashboard_all.html', filterform=filterform,round=round, formData=sum_formdata, user=current_user, form=formdata_list)
    else:
        if filterform.validate_on_submit():
            formdata_list = Form.query.filter(Form.kato_6.startswith(filterform.kato_4.data)).all()
            inspector1 = inspect(Form)
            columns = inspector1.columns.keys()

            sum_formdata = Form(
                **{column: sum(getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in formdata_list)
                    for column in columns}
            )
        else:
            flash(f'Возникла ошибка: {filterform.errors}', category='error')
            formdata_list = Form.query.filter_by(kato_4=current_user.kato_4).all()
            inspector1 = inspect(Form)
            columns = inspector1.columns.keys()

            sum_formdata = Form(
                **{column: sum(getattr(form, column) if isinstance(getattr(form, column), (int, float, Decimal)) else 0 for form in formdata_list)
                    for column in columns}
            )
            return render_template('animal_dashboard_all.html', filterform=filterform,round=round, formData=sum_formdata, user=current_user, form=formdata_list)
    
    return render_template('animal_dashboard_all.html', filterform=filterform,round=round, formData=sum_formdata, user=current_user)


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
        sum_formdata.infrastructure_polivy = round(sum_formdata.infrastructure_polivy / count_form, 2) if count_form != 0 else "Cannot divide by zero"

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
        sum_formdata.credit_average_total = int(sum_formdata.credit_average_total / count_form) if count_form != 0 else "Cannot divide by zero"
        sum_formdata.credit_zalog = round(sum_formdata.credit_zalog / count_form, 2) if count_form != 0 else "Cannot divide by zero"

        return render_template('credits_dashboard_all.html', filterform=filterform, round=round, formData=sum_formdata,
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
            sum_formdata.credit_zalog = round(sum_formdata.credit_zalog / count_form, 2) if count_form != 0 else "Cannot divide by zero"

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

        
        labour_household_size_total_average = round(house_total_dvor_total / counter, 2) if counter != 0 else "Cannot divide by zero"
        labour_average_income_family_total_average = round(labour_average_income_family_total / counter, 2) if counter != 0 else "Cannot divide by zero"
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

            
            labour_household_size_total_average = round(house_total_dvor_total / counter, 2) if counter != 0 else "Cannot divide by zero"
            labour_average_income_family_total_average = round(labour_average_income_family_total / counter, 2) if counter != 0 else "Cannot divide by zero"
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

            
            labour_household_size_total_average = round(house_total_dvor_total / counter, 2) if counter != 0 else "Cannot divide by zero"
            labour_average_income_family_total_average = round(labour_average_income_family_total / counter, 2) if counter != 0 else "Cannot divide by zero"
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
