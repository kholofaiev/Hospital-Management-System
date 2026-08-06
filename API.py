from fastapi import FastAPI, HTTPException, status, Depends
from datetime import date, time, datetime, timedelta
from APIscemas import UserCreate, UserResponse, AppointmentCreate, AppointmentResponse, AppointmentUpdate, Token, create_access_token, oauth2_scheme, verify_access_token, settings
from sqlalchemy.orm import Session
from DatabaseSchema import SessionLocal, User, Appointment
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

# Dependency: Get DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/api/register', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    #Validation Logic
    if user.category == 'patient':
        if user.dob is None or user.specialty is not None:
            raise HTTPException(status_code=409, detail='Patients must have DOB and no specialty')
    elif user.category == 'doctor':
        if user.dob is not None or user.specialty is None:
            raise HTTPException(status_code=409, detail='Doctors must have specialty and no DOB')
    else:
        raise HTTPException(status_code=400, detail=f'Invalid category {user.category}')

    #Create the SQLAlchemy Model Instance
    base_username = f"{user.lastname.lower()}{user.name.lower()}"
    username = base_username
    counter = 1
    
    # Loop until we find a name that doesn't exist in the DB
    while db.query(User).filter(User.username == username).first():
        username = f"{base_username}{counter}"
        counter += 1

    
    db_user = User(
        name=user.name.lower(),
        lastname=user.lastname.lower(),
        username=username,
        category=user.category,
        specialty=user.specialty,
        dob=user.dob,
    )
    db_user.set_password(user.password)

    #Save to Database
    db.add(db_user)
    db.commit()
    db.refresh(db_user) 
    return db_user


@app.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
    ):
    user = db.query(User).filter(User.username == form_data.username.lower()).first()
    
    if not user or not user.check_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorect email or password'
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
    
@app.get("/me", response_model=UserResponse)
def get_current_user(token: str, db: Session = Depends(get_db)):
    user_id = verify_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
            )
    
    try:
        user_id_int = int(user_id)
    except (TypeError, ValueError):
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
            )
    user = db.query(User).filter(User.id == user_id_int).first()
    if not user:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
            )
    return user


@app.get('/api/appointments',response_model=list[AppointmentResponse])
def get_user_appointments(token: str, db: Session = Depends(get_db)):
    user_id = verify_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
            )
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    #Checking user category
    if user.category == 'patient':  # type: ignore
        appointments = db.query(Appointment).filter(Appointment.patient_id == user.id).all()
    elif user.category == 'doctor': # type: ignore
        appointments = db.query(Appointment).filter(Appointment.doctor_id == user.id).all()

    
    return appointments

@app.post('/api/appointments/book', response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(token: str, appointment: AppointmentCreate, db: Session = Depends(get_db)):
    #Check token
    user_id = verify_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
            )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    
    if user.category != 'patient':  # type: ignore
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Only patient can book')
    
    #validate users parametr
    patient = db.query(User).filter(User.id == appointment.patient_id).first()
    doctor = db.query(User).filter(User.id == appointment.doctor_id).first()
    if doctor and patient:
        if doctor.category != 'doctor' or patient.category != 'patient': # type: ignore
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Wrong user categories')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Users not found')
    
    #validate time
    appointment_date = appointment.appointment_date
    appointment_time = appointment.appointment_time
    db_appoitment = Appointment(
        doctor_id = appointment.doctor_id,
        patient_id = appointment.patient_id,
        appointment_date = appointment_date,
        appointment_time = appointment_time,
        diagnosis = None,
        prescription = None,
        status = "opened"
    )
    #Save to Database
    db.add(db_appoitment)
    db.commit()
    db.refresh(db_appoitment) 
    return db_appoitment


@app.patch('/api/appointments/{appointment_id}/update', response_model=AppointmentResponse)
def update_appointment(token:str, appointment_id: int, appointment_data: AppointmentUpdate, db: Session = Depends(get_db)):
    #Check token
    user_id = verify_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
            )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    
    if user.category != 'doctor':  # type: ignore
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Only doctor can eddit appointment')

    
    #appountment logic
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Appoitnment not found')
    
    update_data = appointment_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(appointment, field, value)
    
    db.commit()
    db.refresh(appointment) 
    return appointment
        


