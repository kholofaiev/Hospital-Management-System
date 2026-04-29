from datetime import date, time
from .Appointment import Appointment
from .Doctor import Doctor
from .Patient import Patient
from .Prescription import Prescription
from .Dignosis import Diagnosis
import asyncio

class Hospital():
    def __init__(self, doctors:list, patients:list, apointments = []) -> None:
        self.doctors = doctors
        self.patients = patients
        self.appointments = apointments

    
    def start_appointment(self, doctor:Doctor, patient:Patient):
        doctor.current_appointment = patient.get_history()[-1]
    
    def end_appointment(self, appointment:Appointment):
        print(appointment)
        del appointment
        


        

