import asyncio
from datetime import date, time
from .Appointment import Appointment
from .Doctor import Doctor

class Patient():
    
    def __init__(self, name:str, birth_date:str) -> None:       
        self.name = name
        self.birth_date = birth_date
        self._history = []
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value:str):
        self._name = value.upper()
    
    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        self._birth_date = date.fromisoformat(value)
        
    def __str__(self) -> str:
        return f'Patient {self.name}, D.O.B: {self.birth_date}'
    
    def add_to_history(self, appointment:Appointment): 
        self._history.append(appointment)
        appointment.doctor.appointments.append(appointment)
    
    def print_history(self):
        print('\n'.join(map(str, self._history)))
    
    def get_history(self):
        return self._history
    
    async def create_appointment(self, doctor:Doctor, appointment_date, appointment_time):
        appointment_time = time.fromisoformat(appointment_time)
        appointment_date = date.fromisoformat(appointment_date)
        if  time.fromisoformat('16:00') >= appointment_time >= time.fromisoformat('09:00'):
            await asyncio.sleep(2) #Assume we retrive doctor from DB
            async with doctor.lock:
                if appointment_date not in doctor.booking_times.keys():
                    doctor.booking_times[appointment_date] = dict()
                if appointment_time not in doctor.booking_times[appointment_date]:                
                    appointment = Appointment(self, doctor, appointment_date, appointment_time)
                    doctor.booking_times[appointment_date][appointment_time] = appointment
                    self.add_to_history(appointment)
                    print(f'{self} have booked with Dr. {doctor.name} on {appointment.appointment_date} at {appointment.appointment_time}')
                else:
                    raise Exception('Booking slot is not avalible')
        else:
            raise Exception('Error: Out Buisness Hours')