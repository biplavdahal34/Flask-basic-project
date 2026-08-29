from flask import render_template, request, Blueprint
from flask_project.models import Post


main= Blueprint('main', __name__)

@main.route("/about")
def about():
    return render_template("about.html", title = "About")

@main.route("/home")
@main.route("/")
def home():
    page = request.args.get("page", 1, type=int)
    return render_template("home.html", posts = Post.query.order_by(Post.date_posted.desc()).paginate(page =page, per_page=5))