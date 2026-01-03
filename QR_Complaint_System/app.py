from flask import Flask, render_template, request, redirect, session, flash
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
    conn = sqlite3.connect("database.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- CREATE TABLES ----------------
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Force DB file creation on cloud
with get_db_connection() as conn:
    pass


    # USERS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            gender TEXT,
            student_class TEXT,
            roll_no TEXT,
            id_card TEXT UNIQUE,
            password TEXT,
            role TEXT,
            status TEXT
        )
    """)

    # COMPLAINTS TABLE
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

# ---------------- ADD DEFAULT ADMIN ----------------
def add_default_admin():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (name, gender, student_class, roll_no, id_card, password, role, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("Admin", "NA", "NA", "NA", "ADMIN001", "admin123", "admin", "active"))

    conn.commit()
    conn.close()

add_default_admin()

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        id_card = request.form["id_card"]
        password = request.form["password"]
        role = request.form["role"]

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if user is blocked
        cursor.execute(
            "SELECT status FROM users WHERE id_card=? AND role=?",
            (id_card, role)
        )
        status = cursor.fetchone()

        if status and status[0] == "blocked":
            flash("Your account has been blocked. Please contact the administrator.", "danger")
            conn.close()
            return redirect("/login")

        # Normal login
        cursor.execute("""
            SELECT * FROM users
            WHERE id_card=? AND password=? AND role=? AND status='active'
        """, (id_card, password, role))
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
            flash("Invalid login details", "danger")

    return render_template("login.html")

# ---------------- STUDENT COMPLAINT ----------------
@app.route("/complaint", methods=["GET", "POST"])
def complaint():
    if "role" not in session or session["role"] != "student":
        return redirect("/login")

    location = request.args.get("location", "General")

    if request.method == "POST":
        complaint_text = request.form["complaint"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO complaints (student_id, location, complaint, status)
            VALUES (?, ?, ?, ?)
        """, (session["id_card"], location, complaint_text, "Pending"))
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
    cursor.execute("""
        SELECT * FROM complaints WHERE student_id=?
    """, (session["id_card"],))
    complaints = cursor.fetchall()
    conn.close()

    return render_template("student_complaints.html", complaints=complaints)

# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin")
def admin():
    if "role" not in session or session["role"] != "admin":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM complaints")
    complaints = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM users WHERE role='student'")
    student_count = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "admin.html",
        complaints=complaints,
        student_count=student_count
    )

# ---------------- ADMIN COMPLAINT ACTIONS ----------------
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
    reply_text = request.form["reply"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE complaints SET reply=? WHERE id=?", (reply_text, id))
    conn.commit()
    conn.close()
    return redirect("/admin")

# ---------------- STUDENTS LIST (ADMIN) ----------------
@app.route("/students")
def students():
    if "role" not in session or session["role"] != "admin":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, gender, student_class, roll_no, id_card, status
        FROM users WHERE role='student'
    """)
    students = cursor.fetchall()
    conn.close()

    return render_template("students.html", students=students)

@app.route("/block_student/<student_id>")
def block_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET status='blocked' WHERE id_card=?", (student_id,))
    conn.commit()
    conn.close()
    return redirect("/students")

@app.route("/unblock_student/<student_id>")
def unblock_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET status='active' WHERE id_card=?", (student_id,))
    conn.commit()
    conn.close()
    return redirect("/students")

# ---------------- ADD STUDENT (ADMIN) ----------------
@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if "role" not in session or session["role"] != "admin":
        return redirect("/login")

    message = None

    if request.method == "POST":
        name = request.form["name"]
        gender = request.form["gender"]
        student_class = request.form["student_class"]
        roll_no = request.form["roll_no"]
        student_id = request.form["student_id"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users
                (name, gender, student_class, roll_no, id_card, password, role, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, gender, student_class, roll_no, student_id, password, "student", "active"))
            conn.commit()
            message = "Student added successfully"
        except:
            message = "Student ID already exists"
        conn.close()

    return render_template("add_user.html", message=message)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- QR GENERATION ----------------
@app.route("/generate_qr", methods=["GET", "POST"])
def generate_qr():
    if "role" not in session or session["role"] != "admin":
        return redirect("/login")

    qr_path = None
    os.makedirs("static/qrcodes", exist_ok=True)

    if request.method == "POST":
        location = request.form["location"]

        url = f"http://{request.host}/complaint?location={location}"
        filename = f"{location}.png"
        save_path = os.path.join("static/qrcodes", filename)

        qr = qrcode.make(url)
        qr.save(save_path)
        qr_path = f"/static/qrcodes/{filename}"

    return render_template("generate_qr.html", qr_path=qr_path)

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run()

