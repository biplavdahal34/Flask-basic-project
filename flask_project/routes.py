from flask import render_template,url_for, flash, redirect
from flask_project import app
from flask_project.models import User, Post
from flask_project.forms import Registration, Login

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