import os
import secrets
from flask import render_template,url_for, flash, redirect, request, abort
from flask_project import app,db,bcrypt
from flask_project.models import User, Post
from flask_project.forms import Registration, Login, UpdateAccount, New_post
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/about")
def about():
    return render_template("about.html", title = "About")

@app.route("/home")
@app.route("/")
def home():
    page = request.args.get("page", 1, type=int)
    return render_template("home.html", posts = Post.query.order_by(Post.date_posted.desc()).paginate(page =page, per_page=5))

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
        flash(f'Your Account Has Been Created, Please Login! (˶ˆᗜˆ˵)','success')
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
            flash("Login Failed. Please Try Again! (╥﹏╥)", "danger")
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
    page = request.args.get("page", 1, type=int)
    posts = Post.query.filter_by(author=current_user).order_by(Post.date_posted.desc()).paginate(page =page, per_page=5)
    if form.pfpimage.data:
        f_name = save_picture(form.pfpimage.data)
        current_user.image= f_name
    if form.validate_on_submit():
        if current_user.username != form.username.data or current_user.email != form.email.data:
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash(f'Your Account Has Been Updated! ദ്ദി(๑>؂•̀๑)','success')
            return redirect(url_for("account"))
    elif request.method == "GET" :
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename= "profile_pictures/" + current_user.image)
    print(current_user.image)
    return render_template("account.html", title = "Account", image_file = image_file, form=form, legend ="Update", posts = posts)

@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = New_post()
    if form.validate_on_submit():
        user_post = Post(user_id = current_user.id, title = form.title.data, content = form.body.data)
        db.session.add(user_post)
        db.session.commit()
        flash(f'Your Words Have Been Posted','success')
        return redirect(url_for('home'))
    return(render_template("newpost.html", title="New Post",legend = "Post", form = form ))

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return(render_template("post.html",title = post.title,post=post  ))

@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def modify_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = New_post(title = post.title,body=post.content)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.body.data
        db.session.commit()
        flash(f'Your Post Has Been Updated!','success')
        return redirect(url_for('post', post_id = post_id))
    return(render_template("modify_post.html",title = post.title,legend = "Update",form=form, post=post))

@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Your Post Has Been Deleted','danger')
    return redirect(url_for('home'))
    
@app.route("/user/<string:username>")
def selected_account(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    image_file = url_for('static', filename= "profile_pictures/" + user.image)
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page =page, per_page=5)
    if user.username == current_user.username:
        return redirect(url_for('account'))
    return render_template("selected_account.html", title = username , image_file = image_file, posts = posts, user=user)