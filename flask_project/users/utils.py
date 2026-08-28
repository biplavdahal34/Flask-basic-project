import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from flask_project import app, mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, extn = os.path.splitext(form_picture.filename)
    hex_picture = random_hex + extn
    picturepath = os.path.join(app.root_path, "static/profile_pictures", hex_picture)
    form_picture.save(picturepath)
    return hex_picture

def send_email(user):
    token = user.token_expiry()
    msg = Message('Password Reset Request',sender='ok.2346756@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, please visit the following link:
{url_for('reset_password', token = token, _external=True)}

If your didnot make this request, please ignore it.
'''
    mail.send(msg)