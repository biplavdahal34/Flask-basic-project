from flask import Flask,render_template

app = Flask(__name__)

dummy_post = [{
    "name" : "ricky",
    "age"  : "24",
    "title": "my first post yall",
    "content": "hello, i am rick. nice to meet you all",
    "date" : "May 20, 2026",
},
{
    "name" : "morty",
    "age"  : "16",
    "title": "my post yall",
    "content": "hello, i am morty. nice to meet you all",
    "date" : "june 17, 2026",
},]

@app.route("/support")
def hello_world():
    return render_template("support.html", title = "Support")

@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html", posts = dummy_post)

if __name__ == "__main__":
    app.run(debug=True)