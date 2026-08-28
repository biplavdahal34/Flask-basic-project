import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config["SECRET_KEY"] = "398ro83reufheuf838ue438uff3498eyf"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ok.2346756@gmail.com'
app.config['MAIL_PASSWORD'] = 'pjvs kioq edqh lxkp'
mail = Mail(app)


login_manager.login_view = "login"
login_manager.login_message_category = "info"

from flask_project.users.routes import users
from flask_project.main.routes import main
from flask_project.post.routes import posts

app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(posts)
