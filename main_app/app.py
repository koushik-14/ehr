
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# Route for Homepage (Main Entry Page)
@app.route('/')
def home():
    return render_template('index.html')

# Redirect to Doctor Login Page instead of Doctor Form directly
@app.route('/doctor')
def doctor():
    return redirect("http://127.0.0.1:5000/login")  # Doctor login page

# Redirect to User Website
@app.route('/user')
def user():
    return redirect("http://127.0.0.1:5001")  # Replace with actual user app URL

# Redirect to Insurance Website
@app.route('/insurance')
def insurance():
    return redirect("http://127.0.0.1:5003")  # Replace with actual insurance app URL

if __name__ == '__main__':
    app.run(debug=True, port=5004)  # Running main app on port 5004
