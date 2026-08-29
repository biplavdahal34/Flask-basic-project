from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flask_project import db
from flask_project.models import Post
from flask_project.post.forms import New_post


posts= Blueprint('posts', __name__)

@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = New_post()
    if form.validate_on_submit():
        user_post = Post(user_id = current_user.id, title = form.title.data, content = form.body.data)
        db.session.add(user_post)
        db.session.commit()
        flash(f'Your Words Have Been Posted','success')
        return redirect(url_for('main.home'))
    return(render_template("newpost.html", title="New Post",legend = "Post", form = form ))

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return(render_template("post.html",title = post.title,post=post))

@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
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
        return redirect(url_for('posts.post', post_id = post_id))
    return(render_template("modify_post.html",title = post.title,legend = "Update",form=form, post=post))

@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Your Post Has Been Deleted','danger')
    return redirect(url_for('main.home'))