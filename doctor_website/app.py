
from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
import os
from werkzeug.utils import secure_filename
from twilio.rest import Client

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = "your_secret_key"  # Used for session management

# Twilio Credentials (Replace with actual credentials)
TWILIO_ACCOUNT_SID = "AC62d0382ae811a22b2c67ca0351fee077"
TWILIO_AUTH_TOKEN = "e97d4e3be12368c5930f405885913318"
TWILIO_PHONE_NUMBER = "+18573670895"

# Initialize Doctor Database
def init_doctor_db():
    conn = sqlite3.connect('../database/ehr.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('../database/ehr.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors WHERE email = ? AND password = ?", (email, password))
        doctor = cursor.fetchone()
        conn.close()

        if doctor:
            session['doctor_logged_in'] = True  # Set session variable
            return redirect(url_for('doctor_form'))
        else:
            return render_template('login.html', error="Invalid credentials. Please try again.")

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('doctor_logged_in', None)  # Remove session
    return redirect(url_for('login'))

# Doctor Form Page (Requires Login)
@app.route('/', methods=['GET', 'POST'])
def doctor_form():
    if 'doctor_logged_in' not in session:  # Check if logged in
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username']
        phone = request.form['phone']
        suggestion = request.form['suggestion']
        files = request.files.getlist('file')

        # Validate phone number
        if len(phone) != 10 or not phone.isdigit():
            return "Phone number must be exactly 10 digits."

        # Save files
        file_paths = []
        for file in files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            file_paths.append(filename)

        # Save to database
        conn = sqlite3.connect('../database/ehr.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO doctor_data (username, phone, suggestion, file_path)
            VALUES (?, ?, ?, ?)
        ''', (username, phone, suggestion, ','.join(file_paths)))
        conn.commit()
        conn.close()

        # Send SMS notification
        sms_message = f"Hello {username}, your health record has been updated.\nSuggestion: {suggestion}"
        send_sms(phone, sms_message)

        return "Data submitted successfully!"

    return render_template('doctor_form.html')

# Function to send SMS
def send_sms(phone, message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=f"+91{phone}"  # Adjust country code if needed
    )

if __name__ == '__main__':
    init_doctor_db()
    app.run(debug=True, port=5000)
