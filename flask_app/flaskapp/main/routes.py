from flask import render_template, Blueprint


main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template("home.html")


@main.route("/admin")
def admin():
    return render_template("admin.html", title="Admin")