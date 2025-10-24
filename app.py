import mysql.connector
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="David",
    password="Molefi123#",
    database="school_db"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_application/', methods=['POST'])
def submit_application():
    full_name = request.form['fullName']
    email = request.form['email']
    grade = request.form['grade']
    message = request.form['message']

    cursor = db.cursor()
    query = "INSERT INTO applications (full_name, email, grade, message) VALUES (%s, %s, %s, %s)"
    values = (full_name, email, grade, message)
    cursor.execute(query, values)
    db.commit()
    cursor.close()

    return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return "<h2>✅ Application submitted successfully!</h2>"

if __name__ == '__main__':
    app.run(debug=True)