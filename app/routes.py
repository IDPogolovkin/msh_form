from flask import flash, redirect, render_template, url_for, request
from app.forms import *
from app.models import *
from app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from decimal import Decimal
from sqlalchemy import desc

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
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(kato_6=form.kato_6.data).first()
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
    formdata = Form.query.filter_by(user_id=current_user.id).order_by(desc(Form.creation_date)).first()
    print(formdata)
    form = FormDataForm()
    return render_template('account.html', title = 'Личный кабинет',str=str,form=form,measurement_units=measurement_units, user=current_user, formdata=formdata)

@app.route('/account/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_form(id):
    formdata = Form.query.filter_by(id=id).first()
    form = FormDataForm(obj=formdata)
    if request.method == 'GET':
        return render_template('edit_form.html', form=form, user=current_user, measurement_units=measurement_units, formdata=formdata)
    else:
        if form.validate_on_submit():
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
            db.session.add(new_form)
            db.session.commit()
            flash("Данные успешно изменены!", 'success')
            return redirect(url_for('account'))
        else:
            flash("Данные не изменены! Некорректный формат.", 'danger')
            return render_template('edit_form.html', form=form, user=current_user)

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


@app.route('/form', methods=['POST', 'GET'])
@login_required
def form():
    user = current_user
    form = FormDataForm()
    form_check = Form.query.filter_by(user_id=current_user.id).all()
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
