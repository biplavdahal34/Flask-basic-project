from flask import Flask,render_template,url_for, flash, redirect
from forms import Registration, Login

app = Flask(__name__)
app.config["SECRET_KEY"] = "398ro83reufheuf838ue438uff3498eyf"

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

@app.route("/support")
def support():
    return render_template("support.html", title = "Support")

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

@app.route("/login")
def login():
    form = Login()
    return render_template("login.html", title = "Login", form = form)

if __name__ == "__main__":
    app.run(debug=True)