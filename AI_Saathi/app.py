from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "aisaathi123"

# ---------------- DATABASE ---------------- #

def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- SCHEMES ---------------- #

SCHEMES = [

{
    "name": "NSP Scholarship",
    "education": ["Graduate", "Post Graduate"],
    "max_age": 30,
    "income_limit": 300000,
    "benefit": "Scholarship for students"
},

{
    "name": "PM Internship Scheme",
    "education": ["Graduate"],
    "max_age": 25,
    "income_limit": 800000,
    "benefit": "Internship opportunities"
},

{
    "name": "Skill India Program",
    "education": ["10th", "12th", "Diploma"],
    "max_age": 40,
    "income_limit": 500000,
    "benefit": "Skill training"
},

{
    "name": "AICTE Pragati Scholarship",
    "education": ["Diploma", "Graduate"],
    "max_age": 30,
    "income_limit": 800000,
    "benefit": "Financial support for students"
}

]

# ---------------- ROUTES ---------------- #

@app.route('/')
def home():
    return render_template('login.html')

# Register

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        try:

            conn = sqlite3.connect("database.db")
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO users(name,email,password) VALUES(?,?,?)",
                (
                    request.form['name'],
                    request.form['email'],
                    request.form['password']
                )
            )

            conn.commit()
            conn.close()

            return redirect('/')

        except:
            return "Email already exists"

    return render_template('register.html')

# Login

@app.route('/login', methods=['POST'])
def login():

    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cur.fetchone()

    conn.close()

    if user:

        session['user'] = user[1]

        return redirect('/dashboard')

    return "Invalid Login"

# Dashboard

@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/')

    return render_template(
        'dashboard.html',
        user=session['user']
    )

# Eligibility Check

@app.route('/check', methods=['POST'])
def check():

    age = int(request.form['age'])
    income = int(request.form['income'])
    education = request.form['education']

    eligible = []

    for scheme in SCHEMES:

        education_match = (
            education in scheme["education"]
        )

        age_match = (
            age <= scheme["max_age"]
        )

        income_match = (
            income <= scheme["income_limit"]
        )

        if education_match and age_match and income_match:
            eligible.append(scheme)

    return render_template(
        'schemes.html',
        schemes=eligible,
        age=age,
        income=income,
        education=education
    )

# Logout

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')

# Run

if __name__ == '__main__':
    app.run(debug=True)