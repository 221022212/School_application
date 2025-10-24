# 🏫 School Application System

A full-stack web application built with Flask, MySQL, HTML, and CSS that allows students to apply for school admission online. Submitted applications are stored securely in a MySQL database.

---

## 🚀 Features

- Responsive front-end form for student applications
- Backend integration using Flask
- Data storage in MySQL database
- Confirmation page after successful submission
- Clean folder structure and modular code

---

## 🧱 Technologies Used

- **Frontend**: HTML5, CSS3
- **Backend**: Python 3, Flask
- **Database**: MySQL
- **Version Control**: Git & GitHub

---

## 📁 Project Structure
school_application/
├── app.py                  # Main Flask application
├── config.py               # (Optional) MySQL credentials and config settings
├── requirements.txt        # List of Python dependencies
├── .gitignore              # Git exclusions (e.g. venv, __pycache__)
├── README.md               # Project documentation
│
├── templates/              # HTML templates
│   └── index.html          # Main application form
│   └── thank_you.html      # Confirmation page (optional)
│
├── static/                 # Static assets (CSS, JS, images)
│   └── styles.css          # Styling for the form
│
├── venv/                   # Virtual environment (excluded from Git)
│
└── database/               # (Optional) SQL scripts or backups
    └── schema.sql          # SQL to create the applications table

---

## ⚙️ Setup Instructions

###1. Clone the Repository
bash 
  git clone https://github.com/221022212/school_application.git
  cd school_application
  
  2. Create and Activate Virtual Environment
  '''bash
  python -m venv venv
  venv\Scripts\activate
  
  3. Install Dependencies
  bash '''
  pip install flask mysql-connector-python
  
  4. Configure MySQL
  Open MySQL shell and run:
  CREATE DATABASE school_db;
  USE school_db;
  
  CREATE TABLE applications (
      id INT AUTO_INCREMENT PRIMARY KEY,
      full_name VARCHAR(255),
      email VARCHAR(50),
      grade VARCHAR(50),
      message TEXT
  );
  5. Update  with Your MySQL Credentials
  db = mysql.connector.connect(
      host="localhost",
      user=David,
      password=Molefi123#,
      database="school_db"
  )
  
  6. Run the App
  bash'''
  python app.py
  Visi http://127.0.0.1.5000 in browser to test the form

---
###📬 Future Improvements
• 	Admin dashboard to view submissions
• 	Export applications to CSV
• 	Authentication and login system
• 	Deployment to Render or Railway
• 	Form validation and error handling
• 	Email notifications on submission

👨‍💻 Author
David Molefi Dhlamini
Electrical Engineering student passionate about full-stack development, backend systems, and solving real-world problems through technology.
📍 Bloemfontein, South Africa
🎓 Second-year Electrical Engineering
💡 Focused on building scalable solutions for education and infrastructure

📄 License
This project is open-source and available under the MIT License.
