from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_project import app
from flask_project.models import User


class Registration(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("SIGN UP")

    def validate_username(self, username):
        with app.app_context():
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("The Username Is Already Taken. Please Try Another One")

    def validate_email(self, email):
        with app.app_context():
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("The Email Is Already Taken. Please Try Another One")


class Login(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("LOG IN")
