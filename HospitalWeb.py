from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, time, timedelta
from dotenv import load_dotenv
import os

load_dotenv() 
app = Flask(__name__, template_folder='templates')
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")

#setup database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///hospital.db")
db = SQLAlchemy(app)



 
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    name = db.Column(db.String(15), nullable = False) #on avarage 6.5 symbols for name
    lastname = db.Column(db.String(15), nullable = False) #on avarage 7 synbols per name
    category = db.Column(db.String(50), nullable = False)
    specialty = db.Column(db.String(100), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    password = db.Column(db.String(150), nullable =False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def set_specialty(self, specialty_name):
        if self.category == 'doctor':
            self.specialty = specialty_name.upper()
    

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    doctor = db.relationship('User', foreign_keys=[doctor_id], backref='doctor')                         
    patient = db.relationship('User', foreign_keys=[patient_id], backref='patient')
    
    appointment_date = db.Column(db.Date, nullable = False)
    appointment_time = db.Column(db.Time, nullable = False)
    diagnosis = db.Column(db.String(100), nullable = True)
    prescription = db.Column(db.String(100), nullable = True)
    
    status = db.Column(db.String(6), nullable = False)


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        name = request.form['name']
        lastname = request.form['lastname']
        category = request.form['category']
        if category == 'doctor':
            specialty = request.form['specialty']
        elif category == 'patient':  
            dob = request.form['dob']
        password = request.form['password']

        temp_usr = lastname.lower()+name.lower()
        username = temp_usr
        counter = 1
        # Loop until we find a name that doesn't exist in the DB
        while User.query.filter_by(username=username).first():
            username = f"{temp_usr}{counter}"
            counter += 1
        #add info to database
        new_user = User()
        new_user.name = name
        new_user.lastname = lastname
        new_user.username = username
        new_user.category = category
        if category == 'doctor':
            new_user.specialty = specialty
        elif category == 'patient': 
            dob_str = request.form.get('dob')
            if dob_str:
                dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
                new_user.dob = dob
                
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return render_template('register.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password") 
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    
    user = User.query.filter_by(username=session['username']).first()
    if user.category == 'patient': # type: ignore
        doctors = User.query.filter_by(category='doctor').all()
        appointments = Appointment.query.filter_by(patient_id=user.id) # type: ignore
    elif user.category == 'doctor': # type: ignore
        doctors = None
        appointments = Appointment.query.filter_by(doctor_id=user.id, status='opened') # type: ignore
    else:
        doctors = None
        appointments = None
    
    return render_template('dashboard.html', user=user, doctors=doctors, appointments=appointments)

@app.route('/dashboard/bookappointment', methods=["POST"])
def book_appointment():
    patient = User.query.filter_by(username=session['username']).first()
    doctor = User.query.get(request.form['doctor'])
    appointment_date = date.fromisoformat(request.form['date'])
    appointment_time = time.fromisoformat(request.form['time'])
     #Block bookings for past days
    if appointment_date < date.today():
        flash('Error: You cannot travel to the past!!!')
        return redirect(url_for('dashboard'))
    #Booking gap is 2 hours
    elif appointment_date == date.today() and appointment_time <= (datetime.now() + timedelta(hours=2)).time():
        flash('Error: Booking is closed')
        return redirect(url_for('dashboard'))
    else:
        appointment = Appointment()
        appointment.patient_id = patient.id # type: ignore
        appointment.doctor_id = doctor.id # type: ignore
        appointment.appointment_date = appointment_date
        appointment.appointment_time = appointment_time
        appointment.status = 'opened'
        db.session.add(appointment)
        db.session.commit()
    
    return redirect(url_for('dashboard'))


@app.route('/dashboard/submit', methods=["POST"])
def submit_appointment():
    action = request.form.get('action')
    print(action)
    appointment = Appointment.query.get(request.form['id'])
    if action == 'submit':
        diagnosis = request.form['diagnosis']
        prescription = request.form['prescription']
        if diagnosis:
            appointment.diagnosis = diagnosis # type: ignore
        if prescription:
            appointment.prescription = prescription # type: ignore
    elif action == 'close':
        print('close')
        appointment.status = 'closed' # type: ignore
    
    db.session.commit()
    
    return redirect(url_for('dashboard'))




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)