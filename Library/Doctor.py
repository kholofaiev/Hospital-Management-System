import asyncio
class Doctor():
    
    def __init__(self, name, specialty) -> None:
        self.name = name
        self.specialty = specialty
        self.booking_times = {} #date:{time_slots:Appointment} for checking avalibale slots
        self.current_appointment = None
        self.lock = asyncio.Lock()
        
        self.appointments = [] #for showing in gui
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value:str):
        self._name = value.upper()    
    
    @property
    def specialty(self):
        return self._specialty
    
    @specialty.setter
    def specialty(self, value:str):
        self._specialty = value.upper()
        
    @property
    def current_appointment(self):
        return self._current_appointment
    
    @current_appointment.setter
    def current_appointment(self, appointment):
        self._current_appointment = appointment
    
    
    def start_appointment(self, patient):
        self.current_appointment = patient.get_history()[-1]
    
    def end_appointment(self):
        appointment_result = self.current_appointment
        self.appointments.pop(self.appointments.index(self.current_appointment))
        self.current_appointment = None
        return appointment_result
    
    
    def get_appointmets(self):
        return self.appointments
    
    def __str__(self) -> str:
        return f'Dr. {self.name}\nSpeciality: {self.specialty}'