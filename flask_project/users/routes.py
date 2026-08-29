from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_project import db, bcrypt
from flask_project.models import User, Post
from flask_project.users.forms import Registration, Login, UpdateAccount,Request_reset_form, Password_reset_form
from flask_project.users.utils import save_picture, send_email
from flask import Blueprint


users= Blueprint('users', __name__)

@users.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Registration()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your Account Has Been Created, Please Login! (˶ˆᗜˆ˵)','success')
        return redirect(url_for("users.login"))
    return render_template("register.html", title = "Register", form = form)

@users.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        next_page = request.args.get('next')
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Login Successful!", "success")
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Login Failed. Please Try Again! (╥﹏╥)", "danger")
    return render_template("login.html", title = "Login", form = form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account",methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccount()
    page = request.args.get("page", 1, type=int)
    posts = Post.query.filter_by(author=current_user).order_by(Post.date_posted.desc()).paginate(page =page, per_page=5)
    if form.validate_on_submit():
        if form.pfpimage.data:
            f_name = save_picture(form.pfpimage.data)
            current_user.image= f_name
            db.session.commit()
        if current_user.username != form.username.data or current_user.email != form.email.data:
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash(f'Your Account Has Been Updated! ദ്ദി(๑>؂•̀๑)','success')
            return redirect(url_for("users.account"))
    elif request.method == "GET" :
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename= "profile_pictures/" + current_user.image)
    return render_template("account.html", title = "Account", image_file = image_file, form=form, legend ="Update", posts = posts, user=current_user)


@users.route("/user/<string:username>")
def selected_account(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    image_file = url_for('static', filename= "profile_pictures/" + user.image)
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page =page, per_page=5)
    if user.username == current_user.username:
        return redirect(url_for('users.account'))
    return render_template("selected_account.html", title = username , image_file = image_file, posts = posts, user=user)



@users.route("/reset_request", methods=['GET','POST'])
def reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = Request_reset_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_email(user)
            flash('An Email Has Been Sent To Your Email Address!', 'info')
            return redirect(url_for('users.login'))
        else:
            flash('Email Does Not Exist', 'danger')
            return redirect(url_for('users.reset'))
    return render_template("reset_request.html", title="Reset Form", form=form)

@users.route("/reset_request/<string:token>",methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_token(token)
    if user is None:
        flash('That Is An Invalid Or Expired Token', 'warning')
        return redirect(url_for('users.reset'))
    form = Password_reset_form()
    if form.validate_on_submit():
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            user.password = hashed_password
            db.session.commit()
            flash(f'Your Password Has Been Reset! (˶ˆᗜˆ˵)','success')
            return redirect(url_for("useers.login"))
    return render_template("reset_password.html", title = "Reset Password" , form=form, user=user)