from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired


app = Flask(__name__)
app.config['DEBUG'] = True


from app import routes
