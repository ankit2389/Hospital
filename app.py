from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import mysql.connector
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="hospital"
    )

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# SIGN UP (Register)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_data VALUES (%s, %s)", (username, password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

# SIGN IN (Login)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_data WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials. Try again!"
    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

# Show Administration Details
@app.route('/show/administration')
def show_administration():
    if 'username' in session:
        return render_template('administration.html', username=session['username'])
    return redirect(url_for('login'))

# Show Doctor Details
@app.route('/show/doctors')
def show_doctors():
    if 'username' in session:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM doctor_details")
        doctors = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('doctors.html', doctors=doctors)
    return redirect(url_for('login'))

# Add New Doctor Form Page
@app.route('/add/doctor', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        name = request.form['name']
        specialisation = request.form['specialisation']
        age = request.form['age']
        address = request.form['address']
        contact = request.form['contact']
        fees = request.form['fees']
        monthly_salary = request.form['monthly_salary']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO doctor_details VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (name, specialisation, age, address, contact, fees, monthly_salary))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('show_doctors'))
    return render_template('add_doctor.html')

# delete doctor record
@app.route('/delete_doctors', methods=['POST'])
def delete_doctors():
    doctor_names = request.json.get('doctor_names')  # Get the list of doctor names
    if doctor_names:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Use WHERE Name IN (...) for batch deletion
        format_strings = ','.join(['%s'] * len(doctor_names))
        query = f"DELETE FROM doctor_details WHERE Name IN ({format_strings})"
        cursor.execute(query, tuple(doctor_names))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Records deleted successfully!'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'No records selected!'}), 400

# Show Nurse Details
@app.route('/show/nurses')
def show_nurses():
    if 'username' in session:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM nurse_details")
        nurses = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('nurses.html', nurses=nurses)
    return redirect(url_for('login'))

# Add New Nurse Form Page
@app.route('/add/nurse', methods=['GET', 'POST'])
def add_nurse():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        address = request.form['address']
        contact = request.form['contact']
        monthly_salary = request.form['monthly_salary']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO nurse_details VALUES (%s, %s, %s, %s, %s)",
                       (name, age, address, contact, monthly_salary))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('show_nurses'))
    return render_template('add_nurse.html')

# Delete Nurse Records
@app.route('/delete_nurses', methods=['POST'])
def delete_nurses():
    nurse_names = request.json.get('nurse_names')
    if nurse_names:
        conn = get_db_connection()
        cursor = conn.cursor()
        format_strings = ','.join(['%s'] * len(nurse_names))
        query = f"DELETE FROM nurse_details WHERE Name IN ({format_strings})"
        cursor.execute(query, tuple(nurse_names))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Nurse records deleted successfully!'}), 200
    return jsonify({'status': 'error', 'message': 'No records selected!'}), 400

# Show Worker Details
@app.route('/show/workers')
def show_workers():
    if 'username' in session:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM other_worker_details")
        workers = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('workers.html', workers=workers)
    return redirect(url_for('login'))

# Add New Worker Form Page
@app.route('/add/worker', methods=['GET', 'POST'])
def add_worker():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        address = request.form['address']
        contact = request.form['contact']
        monthly_salary = request.form['monthly_salary']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO other_worker_details VALUES (%s, %s, %s, %s, %s)",
                       (name, age, address, contact, monthly_salary))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('show_workers'))
    return render_template('add_worker.html')

# Delete Worker Records
@app.route('/delete_workers', methods=['POST'])
def delete_workers():
    worker_names = request.json.get('worker_names')
    if worker_names:
        conn = get_db_connection()
        cursor = conn.cursor()
        format_strings = ','.join(['%s'] * len(worker_names))
        query = f"DELETE FROM other_worker_details WHERE Name IN ({format_strings})"
        cursor.execute(query, tuple(worker_names))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Worker records deleted successfully!'}), 200
    return jsonify({'status': 'error', 'message': 'No records selected!'}), 400

# Show Patient Details
@app.route('/show/patients')
def show_patients():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT Name, Gender, Age, Address, Doctor_recommended, Room FROM patient_details")
    patients = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('patients.html', patients=patients)

# Add New Patient Form Page
@app.route('/add/patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        age = request.form['age']
        address = request.form['address']
        doctor = request.form['doctor']
        room = request.form['room']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO patient_details VALUES (%s, %s, %s, %s, %s, %s)",
                       (name, gender, age, address, doctor, room))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('show_patients'))
    return render_template('add_patient.html')

# Delete Patient Records
@app.route('/delete_patients', methods=['POST'])
def delete_patients():
    patient_names = request.json.get('patient_names')  # Get the list of patient names
    if patient_names:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Use WHERE Name IN (...) for batch deletion
        format_strings = ','.join(['%s'] * len(patient_names))
        query = f"DELETE FROM patient_details WHERE Name IN ({format_strings})"
        cursor.execute(query, tuple(patient_names))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Patient records deleted successfully!'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'No records selected!'}), 400

@app.route('/discharge_patient', methods=['POST'])
def discharge_patient():
    name = request.form['name']
    days = int(request.form['days'])
    charges = int(request.form['charges'])
    paid = request.form['paid']

    # Calculate the bill
    total_charges = days * charges
    gst = 0.25 * total_charges
    total_bill = total_charges + gst

    if paid == 'y':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patient_details WHERE Name = %s", (name,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status': 'success', 'message': f"Patient {name} successfully discharged.", 'total_bill': total_bill})
    else:
        return jsonify({'status': 'pending', 'message': f"Patient {name} has a pending bill.", 'total_bill': total_bill})


# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
