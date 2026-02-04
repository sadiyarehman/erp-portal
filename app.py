from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = "erp_secret_key"  # required for session


def load_users():
    with open("users.json", "r") as f:
        return json.load(f)


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()
        student = users.get("student")

        if student["username"] == username and student["password"] == password:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
