from flask import Flask, render_template, request, redirect, session
import sqlite3
import qrcode
import os

app = Flask(__name__)
app.secret_key = "simple_secret_key"

# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect("/login")

# ---------------- DATABASE CONNECTION ----------------
def get_db_connection():
    return sqlite3.connect("database.db")

# ---------------- CREATE TABLES ----------------
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_card TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)

    # Complaints table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            location TEXT,
            complaint TEXT,
            status TEXT,
            reply TEXT
        )
    """)

    conn.commit()
    conn.close()

create_tables()

# ---------------- ADD DEFAULT USERS ----------------
def add_default_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO users (id_card, password, role) VALUES (?, ?, ?)",
        ("ADMIN001", "admin123", "admin")
    )

    cursor.execute(
        "INSERT OR IGNORE INTO users (id_card, password, role) VALUES (?, ?, ?)",
        ("STU101", "student123", "student")
    )

    conn.commit()
    conn.close()

add_default_users()

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        id_card = request.form["id_card"]
        password = request.form["password"]
        role = request.form["role"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE id_card=? AND password=? AND role=?",
            (id_card, password, role)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            session["id_card"] = id_card
            session["role"] = role

            if role == "admin":
                return redirect("/admin")
            else:
                return redirect("/complaint?location=General")
        else:
            error = "Invalid Login Details"

    return render_template("login.html", error=error)

# ---------------- STUDENT COMPLAINT FORM ----------------
@app.route("/complaint", methods=["GET", "POST"])
def complaint():
    if "role" not in session or session["role"] != "student":
        return redirect("/login")

    location = request.args.get("location", "General")

    if request.method == "POST":
        user_complaint = request.form["complaint"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO complaints (student_id, location, complaint, status) VALUES (?, ?, ?, ?)",
            (session["id_card"], location, user_complaint, "Pending")
        )
        conn.commit()
        conn.close()

        return redirect("/mycomplaints")

    return render_template("complaint.html", location=location)

# ---------------- STUDENT COMPLAINT HISTORY ----------------
@app.route("/mycomplaints")
def my_complaints():
    if "role" not in session or session["role"] != "student":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM complaints WHERE student_id=?",
        (session["id_card"],)
    )
    data = cursor.fetchall()
    conn.close()

    return render_template("student_complaints.html", complaints=data)

# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin")
def admin():
    if "role" not in session or session["role"] != "admin":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints")
    data = cursor.fetchall()
    conn.close()

    return render_template("admin.html", complaints=data)

# ---------------- ADMIN ACTIONS ----------------
@app.route("/resolve/<int:id>")
def resolve(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE complaints SET status='Resolved' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/admin")

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM complaints WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/admin")

@app.route("/reply/<int:id>", methods=["POST"])
def reply(id):
    admin_reply = request.form["reply"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE complaints SET reply=? WHERE id=?",
        (admin_reply, id)
    )
    conn.commit()
    conn.close()
    return redirect("/admin")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- ADMIN QR GENERATION ----------------
@app.route("/generate_qr", methods=["GET", "POST"])
def generate_qr():
    if "role" not in session or session["role"] != "admin":
        return redirect("/login")

    qr_path = None
    os.makedirs("static/qrcodes", exist_ok=True)

    if request.method == "POST":
        location = request.form["location"]
        purpose = request.form["purpose"]  # used for explanation / future scope

        url = f"http://{request.host}/complaint?location={location}"

        filename = f"{location}.png"
        save_path = os.path.join("static/qrcodes", filename)

        qr = qrcode.make(url)
        qr.save(save_path)

        qr_path = f"/static/qrcodes/{filename}"

    return render_template("generate_qr.html", qr_path=qr_path)

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
