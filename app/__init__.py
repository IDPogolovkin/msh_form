from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'b982c2edf1a2f17e9e06c49fb027e8d1'
# app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #Сука если ты редачишь на локалке закоменти строку сверху и раскомменти эту
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


from app import routes
