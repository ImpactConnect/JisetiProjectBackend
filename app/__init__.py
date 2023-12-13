from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from models import User
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
app.config['SECRET_KEY'] = '\r/5\xe1\xbbq\xad\xa4\xb0-\xc3Z*)B\x10\x18%\xe7\xc7\xb5\xfd;\xa4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

from app import routes
