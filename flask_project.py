from datetime import datetime
from flask import Flask,render_template,url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import Registration, Login

app = Flask(__name__)
app.config["SECRET_KEY"] = "398ro83reufheuf838ue438uff3498eyf"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique = True, nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    image = db.Column(db.String(20), nullable = False, default= "default.jpeg")
    password = db.Column(db.String(60), nullable = False)
    posts = db.relationship('Post', backref="author", lazy = True)

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

dummy_post = [{
    "name" : "ricky",
    "age"  : "24",
    "title": "First Post",
    "content": "hello, i am rick. nice to meet you all",
    "date" : "May 20, 2026",
},
{
    "name" : "morty",
    "age"  : "16",
    "title": "New post, Hello",
    "content": "hello, i am morty. nice to meet you all",
    "date" : "june 17, 2026",
},]

@app.route("/about")
def about():
    return render_template("about.html", title = "About")

@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html", posts = dummy_post)

@app.route("/register",methods=['GET','POST'])
def register():
    form = Registration()
    if form.validate_on_submit():
        flash(f'Account Created For {form.username.data}!','success')
        return redirect(url_for("home"))
    return render_template("register.html", title = "Register", form = form)

@app.route("/login",methods=['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        if form.email.data == "biplav123@gmail.com" and form.password.data == "password":
            flash("Welcome", "success")
            return redirect(url_for("home"))
        else:
            flash("Login Failed. Please Try Again", "danger")
    return render_template("login.html", title = "Login", form = form)

if __name__ == "__main__":
    app.run(debug=True)