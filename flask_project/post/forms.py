from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class New_post(FlaskForm):
    title = TextAreaField("Title", validators=[DataRequired(), Length(max=50)])
    body = TextAreaField("Body", validators=[DataRequired(), Length(max=3000)])
    submit = SubmitField("Post")