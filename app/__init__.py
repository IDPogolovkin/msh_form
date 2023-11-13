from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import pathlib
import os
from dotenv import load_dotenv
from db_settings import *


# host =  os.getenv('HOST')
# port =  os.getenv('PORT') 
# database =  os.getenv('DATABASE_POSTGRES')
# user =  os.getenv('USER_POSTGRES')
# password = os.getenv('PASSWORD_POSTGRES')

host =  'localhost'
port = '5432'
database =  'postgres'
user =  'postgres'
password = 'Nitec123'

print(host)
print(type(host))

app = Flask(__name__, static_folder=os.path.join(pathlib.Path().resolve(), 'app', 'static'))
app.config['SECRET_KEY'] = 'b982c2edf1a2f17e9e06c49fb027e8d1'
# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}:{port}/{database}' # коннект для постгрес (настройки в db_settings.py). не забудь закомментить sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG'] = True
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_USERNAME'] = ''
# app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False


mail= Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' 
login_manager.login_message_category = 'info'
login_manager.login_message = 'Войдите в аккаунт, чтобы получить доступ к этой странице'


from app import routes
