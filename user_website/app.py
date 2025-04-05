
from flask import Flask, request, render_template, send_from_directory, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"
UPLOAD_FOLDER = '../doctor_website/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        phone = request.form['phone']

        # Ensure phone number is exactly 10 digits
        if len(phone) != 10 or not phone.isdigit():
            return "Phone number must be exactly 10 digits."

        conn = sqlite3.connect('../database/ehr.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT suggestion, file_path
            FROM doctor_data
            WHERE username = ? AND phone = ?
        ''', (username, phone))
        data = cursor.fetchall()
        conn.close()

        if data:
            session['username'] = username  # Store session for logout functionality
            return render_template('user_data.html', data=[(s, f.split(',')) for s, f in data])
        else:
            return "Invalid username or phone number."

    return render_template('login.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# New route for searching diseases
@app.route('/search', methods=['GET', 'POST'])
def search():
    results = None
    if request.method == 'POST':
        disease_name = request.form['disease'].strip().lower()

        conn = sqlite3.connect('../database/ehr.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT symptoms, suggestions FROM disease_info WHERE disease = ?
        ''', (disease_name,))
        results = cursor.fetchone()
        conn.close()

    return render_template('search.html', results=results)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
