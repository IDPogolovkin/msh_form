from flask import flash, redirect, render_template, url_for, request
from app.forms import *
from app.models import *
from app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from decimal import Decimal

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
    formdata = Form.query.filter_by(user_id=current_user.id).all()
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
            form_data['modified_date'] = datetime.now(timezone(timedelta(hours=6)))
            Form.query.filter_by(id=id).update(form_data)
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
        return render_template('creditors.html', form=form, user=current_user)
    else:
        if form.validate_on_submit():
            creditor = Creditor(
                user_kato = current_user.kato_6,
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
            )
            db.session.add(creditor)
            db.session.commit()
            flash("Кредитор успешно добавлен!", 'success')
            return redirect(url_for('add_creditors'))
        
@app.route('/all-creditors', methods=['GET'])
@login_required
def all_creditors():
    creditors = Creditor.query.filter_by(user_kato=current_user.kato_6).all()
    return render_template('all_creditors.html', creditors=creditors, user=current_user)


@app.route('/form', methods=['POST', 'GET'])
@login_required
def form():
    user = current_user
    form = FormDataForm()
    if request.method == "GET":
        return render_template('ms_form.html', form=form, measurement_units=measurement_units, user=user)
    else:
        if form.validate_on_submit():

            user_id = current_user.id
            form_data = {
                'user_id': user_id,
                'form_year': datetime.now().year,
                **{field.name: getattr(form, field.name).data for field in form if field.name not in ['csrf_token', 'submit']}
            }
            formdata = Form(**form_data)
            db.session.add(formdata)
            db.session.commit()
            flash("Форма успешено добавлена!", 'success')
            return redirect(url_for('account'))
        else:
            print(form.errors)
            print(current_user)
            flash("Форма заполнена некорректно или отсутствуют необходимые поля.", 'danger')
    return render_template('ms_form.html', title='Форма отчетности МСХ',form=form, measurement_units=measurement_units, user=current_user)
