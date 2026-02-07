from flask import Flask, render_template, request, redirect, session,url_for
import json
import sqlite3

app = Flask(__name__)
app.secret_key = "erp_secret_key"


# ---------- HELPERS ----------

def load_users():
    with open("users.json", "r") as f:
        return json.load(f)


def load_erp_data():
    with open("erp_data.json", "r") as f:
        return json.load(f)

def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn



# ---------- AUTH ROUTES ----------

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()

        if user:
            session["user"] = user["email"]
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    session.clear()
    return redirect("/login")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()

        # check if exists
        existing = db.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()

        if existing:
            return render_template("register.html", error="User already exists")

        db.execute(
            "INSERT INTO users(email,password) VALUES(?,?)",
            (email,password)
        )
        db.commit()

        return redirect("/login")

    return render_template("register.html")


# ---------- DASHBOARD ----------

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    data = load_erp_data()
    return render_template("dashboard.html", student=data["student"])


# ---------- ERP MODULES ----------

@app.route("/academics")
def academics():
    if "user" not in session:
        return redirect("/login")

    data = load_erp_data()
    return render_template(
        "academics.html",
        academics=data["academics"]
    )


@app.route("/attendance")
def attendance():
    if "user" not in session:
        return redirect("/login")

    data = load_erp_data()
    total = data["attendance"]["total_classes"]
    attended = data["attendance"]["attended_classes"]
    percentage = round((attended / total) * 100, 2)

    return render_template(
        "attendance.html",
        total=total,
        attended=attended,
        percentage=percentage
    )


@app.route("/placements")
def placements():
    if "user" not in session:
        return redirect("/login")

    data = load_erp_data()
    return render_template(
        "placements.html",
        placements=data["placements"]
    )


# ---------- RUN ----------

if __name__ == "__main__":
    app.run(debug=True)
