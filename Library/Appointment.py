from .Prescription import Prescription
from datetime import date, time
from .Dignosis import Diagnosis

class Appointment():
    def __init__(self, patient, doctor, appointment_date:date, appointment_time:time) -> None:
        self.doctor = doctor
        self.patient = patient
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.current_diagnosis = None
    
    def form_diagnosis(self, diagnosis_name, treatment):
        self.current_diagnosis = Diagnosis(diagnosis_name, treatment)
    
    def prescribe(self, **prescription_meds):
        return Prescription(prescription_meds)
    
    def __str__(self) -> str:
        return f'Appointment details:\nDate:\t{self.appointment_date}, {self.appointment_time}\n{self.patient}\n{self.doctor}\n{self.current_diagnosis}'
    