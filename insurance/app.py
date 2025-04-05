from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"
UPLOAD_FOLDER = "static/uploads"
DB_PATH = "database/insurance.db"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Home page redirects to login
@app.route("/")
def home():
    return redirect(url_for("login"))

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["email"] = email
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password", "error")

    return render_template("login.html")

# Dashboard route (data submission)
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "email" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        insurance_name = request.form["insurance_name"]
        insurance_company = request.form["insurance_company"]
        file = request.files["file"]

        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO insurance_data (email, name, phone, insurance_name, insurance_company, file_path)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (session["email"], name, phone, insurance_name, insurance_company, file_path))
            conn.commit()
            conn.close()

            flash("Data submitted successfully!", "success")

    return render_template("dashboard.html")

# View submitted data
@app.route("/view_data")
def view_data():
    if "email" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM insurance_data WHERE email = ?", (session["email"],))
    records = cursor.fetchall()
    conn.close()

    return render_template("view_data.html", records=records)

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# Run app
if __name__ == "__main__":
    app.run(debug=True, port=5003)
