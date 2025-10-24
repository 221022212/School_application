import mysql.connector
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = "Molefi123#"


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'jpg', 'jpeg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/achievements')
def achievements():
    return render_template('achievements.html')

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

    # Store email in session so we can fetch status
    session['student_logged_in'] = True
    session['username'] = email

    return redirect(url_for('check_status'))



@app.route('/thank_you')
def thank_you():
    return "<h2>✅ Application submitted successfully!</h2>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        cursor.close()

        session['student_logged_in'] = True
        session['username'] = username
        return redirect(url_for('apply'))

    return render_template('register.html')

@app.route('/student_login', methods=['GET', 'POST'])
def login_student():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['student_logged_in'] = True
            session['username'] = username
            return redirect(url_for('apply'))
        else:
            return render_template('student_login.html', error='Invalid credentials')

    return render_template('student_login.html')

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if not session.get('student_logged_in'):
        return redirect(url_for('login_student'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM applications WHERE email=%s", (session['username'],))
    existing = cursor.fetchone()

    if existing:
        cursor.close()
        return redirect(url_for('check_status'))

    if request.method == 'POST':
        full_name = request.form['full_name']
        email = session['username']
        grade = request.form['grade']
        message = request.form['message']
        file = request.files['document']

        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO applications (full_name, email, grade, message, document)
            VALUES (%s, %s, %s, %s, %s)
        """, (full_name, email, grade, message, filename))
        db.commit()
        cursor.close()

        return redirect(url_for('check_status'))

    return render_template('apply.html')


@app.route('/status')
def check_status():
    if not session.get('student_logged_in'):
        return redirect(url_for('login_student'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM applications WHERE email=%s", (session['username'],))
    application = cursor.fetchone()
    cursor.close()

    return render_template('status.html', application=application)

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM applications")
    applications = cursor.fetchall()
    cursor.close()
    return render_template('admin.html', applications=applications)

@app.route('/update_status', methods=['POST'])
def update_status():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    app_id = request.form['id']
    status = request.form['status']

    cursor = db.cursor()
    cursor.execute("UPDATE applications SET status=%s WHERE id=%s", (status, app_id))
    db.commit()
    cursor.close()

    return redirect(url_for('admin_dashboard'))
@app.route('/delete_application/<int:app_id>', methods=['POST'])
def delete_application(app_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    cursor = db.cursor()
    cursor.execute("DELETE FROM applications WHERE id = %s", (app_id,))
    db.commit()
    cursor.close()

    return redirect(url_for('admin_dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)