from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flask_project.models import User, current_app


class Registration(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("SIGN UP")

    def validate_username(self, username):
        with current_app.app_context():
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("The Username Is Already Taken. Please Try Another One")

    def validate_email(self, email):
        with current_app.app_context():
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("The Email Is Already Taken. Please Try Another One")


class Login(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("LOG IN")


class UpdateAccount(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    pfpimage = FileField("Update Profile Picture", validators=[FileAllowed(['png','jpg','webp'])])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("The Username Is Already Taken. Please Try Another One")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("The Email Is Already Taken. Please Try Another One")

class Request_reset_form(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")
    
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('An Account With This Email Doesnot Exist!')


class Password_reset_form(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Confirm")