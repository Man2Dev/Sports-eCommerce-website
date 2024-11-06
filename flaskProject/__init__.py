from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:nope@localhost/software_development_srh'
app.config['SECRET_KEY'] = 'jjkasbdjhbfjbh23jhbhaskasddb1299910'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

import routes

with app.app_context():
    db.create_all()


