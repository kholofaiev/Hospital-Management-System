import os
from sqlalchemy import create_engine, Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash

#Setup Engine
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///instance/hospital.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

#Session and Base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
class Base (DeclarativeBase):
    pass


#Models
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(40), unique=True, nullable=False)
    name = Column(String(15), nullable=False)
    lastname = Column(String(15), nullable=False)
    category = Column(String(50), nullable=False)
    specialty = Column(String(100), nullable=True)
    dob = Column(Date, nullable=True)
    password = Column(String(150), nullable=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(pwhash=self.password, password=password) # type: ignore

class Appointment(Base):
    __tablename__ = "appointment"
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    patient_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
   
    doctor = relationship('User', foreign_keys=[doctor_id], backref='doctor_appointments')
    patient = relationship('User', foreign_keys=[patient_id], backref='patient_appointments')
    
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    diagnosis = Column(String(100), nullable=True)
    prescription = Column(String(100), nullable=True)
    status = Column(String(6), nullable=False)