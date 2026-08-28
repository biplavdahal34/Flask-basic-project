from itsdangerous import URLSafeTimedSerializer as Serializer
from flask_project import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique = True, nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    image = db.Column(db.String(20), nullable = False, default= "default.jpg")
    password = db.Column(db.String(60), nullable = False)
    posts = db.relationship('Post', backref="author", lazy = True)

    def token_expiry(self):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id':self.id}, salt='password-reset')
    @staticmethod
    def verify_token(token, max_age=120):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, salt='password-reset', max_age=max_age)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"