import os
import secrets
from flask import render_template,url_for, flash, redirect, request
from flask_project import app,db,bcrypt
from flask_project.models import User, Post
from flask_project.forms import Registration, Login, UpdateAccount, New_post
from flask_login import login_user, current_user, logout_user, login_required
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Registration()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your Account Has Been Created, Please Login!','success')
        return redirect(url_for("login"))
    return render_template("register.html", title = "Register", form = form)

@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        next_page = request.args.get('next')
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login Failed. Please Try Again", "danger")
    return render_template("login.html", title = "Login", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, extn = os.path.splitext(form_picture.filename)
    hex_picture = random_hex + extn
    picturepath = os.path.join(app.root_path, "static/profile_pictures", hex_picture)
    form_picture.save(picturepath)
    return hex_picture


@app.route("/account",methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccount()
    if form.pfpimage.data:
        f_name = save_picture(form.pfpimage.data)
        current_user.image= f_name
    if form.validate_on_submit():
        if current_user.username != form.username.data or current_user.email != form.email.data:
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash(f'Your Account Has Been Updated','success')
            return redirect(url_for("account"))
    elif request.method == "GET" :
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename= "profile_pictures/" + current_user.image)
    print(current_user.image)
    return render_template("account.html", title = "Account", image_file = image_file, form=form, legend ="Update")

@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = New_post()
    if form.validate_on_submit():
        user_post = Post(user_id = current_user.id, title = form.title.data, content = form.body.data)
        db.session.add(user_post)
        db.session.commit()
        flash(f'Your Words Have Been Posted','success')
    return(render_template("newpost.html", title="New Post",legend = "Post", form = form ))