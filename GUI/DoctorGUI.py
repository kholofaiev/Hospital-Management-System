import tkinter as tk
from tkinter import messagebox, ttk
from Library.Hospital import Doctor, Appointment, Patient
from datetime import date, time

class DoctorDashboard(tk.Toplevel):
    def __init__(self, doctor:Doctor, patients:list):
        super().__init__()
        
        # Initialize the Doctor instance
        self.doctor = doctor
        self.appointments = []
        for patient in patients:
            if len(patient._history) > 0:
                self.appointments.append(patient._history[-1])
        
        self.title(f"Dashboard: {self.doctor.name}")
        self.geometry("450x600")

        self.profile = DoctorProfile(self, self.doctor)
        self.profile.pack(fill="x", padx=10, pady=10)
        
        self.appointmentcomtrol = AppointmentControl(self)
        self.appointmentselect = AppointmentSelect(self, self.doctor, self.appointmentcomtrol)
        self.appointmentselect.pack(fill="x", padx=10, pady=10)
        self.appointmentcomtrol.pack(fill="x", padx=10, pady=10)
        

        
class DoctorProfile(ttk.LabelFrame):
    def __init__(self, parent, doctor:Doctor):
        super().__init__(parent, text="Doctor Profile", padding=10)
        self.doctor = doctor
        
        tk.Label(self, text="Name:").grid(row=0,column=0)
        tk.Label(self, text=f'Dr. {self.doctor.name}', font=("Arial", 10, "bold")).grid(row=0, column=1,sticky='w') 
        tk.Label(self, text="Speciality:").grid(row=1, column=0)
        tk.Label(self, text=self.doctor.specialty).grid(row=1,column=1, padx=10, sticky='w')    

class AppointmentSelect(ttk.LabelFrame):
    def __init__(self, parent, doctor:Doctor, controlpanel):
        super().__init__(parent, text="Appointments", padding=10)
        self.doctor = doctor
        self.appointments = self.doctor.get_appointmets()
        self.controlpanel = controlpanel
        
        tk.Label(self, text="Select Patient to Call In:").grid(row=0,column=0,sticky='w')
        patient_names = [ap.patient.name for ap in self.appointments]
        self.patient_selector = ttk.Combobox(self, values=patient_names, state="readonly")
        if patient_names:
            self.patient_selector.current(0)
        self.patient_selector.grid(row=0,column=1)
        
        self.start_btn = tk.Button(self, text='Start Appointment', command=self.begin_appointment)
        self.start_btn.grid(row=1,column=0, columnspan=2, sticky='we', pady=5)
        self.end_btn = tk.Button(self, text='End appointment', command=self.end_appointment, state='disabled')
        self.end_btn.grid(row=3, column=0, columnspan=2, pady=10, sticky='we')
        
    
    def begin_appointment(self):
        self.current_appointment = self.appointments[self.patient_selector.current()]
        self.doctor.start_appointment(self.current_appointment.patient)
        self.controlpanel.change_status(True, self.current_appointment)
        self.patient_selector.configure(state='disabled')
        self.start_btn.configure(state='disabled')
        self.end_btn.configure(state='normal')
    
    def end_appointment(self):
        self.appointment = self.doctor.end_appointment()
        self.controlpanel.change_status(False)
        self.end_btn.configure(state='disabled')
        self.start_btn.configure(state='normal')
        self.patient_selector.configure(state='normal')
        messagebox.showinfo('Appointment details', self.appointment)




class AppointmentControl(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Current Appointment", padding=10)
        
        self.status_frame = tk.Frame(self)
        self.status_var = tk.StringVar(value="Status: Idle")
        self.patient_info = tk.StringVar(value='No patient being seen.')
        ttk.Label(self.status_frame, textvariable=self.status_var, font=("Arial", 10, "italic")).pack(pady=5)
        ttk.Label(self.status_frame, textvariable=self.patient_info, font=("Arial", 10, "italic")).pack(pady=5)
        self.status_frame.pack(pady=10)
        
        self.control = tk.Frame(self)
        tk.Label(self.control, text="Diagnosis name:").grid(row=0,column=0)
        self.diagnosis_name = tk.Entry(self.control, state='disabled')
        self.diagnosis_name.grid(row=0,column=1, pady=5, padx=5)
        tk.Label(self.control, text="Prescription (name:dosage)").grid(row=1, column=0)
        self.prescription_entry = tk.Entry(self.control, state='disabled')
        self.prescription_entry.grid(row=1,column=1, pady=5, padx=5)
        self.form_diagnosis_btn = tk.Button(self.control, text="Form Diagnosis", state='disabled', command=self.form_diagnosis)
        self.form_diagnosis_btn.grid(row=2,column=0, columnspan=2, sticky='we')
        self.control.pack()
        
        
    def change_status(self, status:bool, appointment = None):
        if status and appointment:
            self.appointment = appointment
            self.status_var.set('Status: IN SESSION')
            self.patient_info.set(f'Now seeing {self.appointment.patient}')    
            self.diagnosis_name.configure(state='normal')
            self.prescription_entry.configure(state='normal')
            self.form_diagnosis_btn.configure(state='normal')
        else:
            self.status_var.set('Status Idle')
            self.patient_info.set('No patient being seen.')
            self.diagnosis_name.delete(0,tk.END)
            self.diagnosis_name.configure(state='disabled')
            self.prescription_entry.delete(0,tk.END)
            self.prescription_entry.configure(state='disabled')
            self.form_diagnosis_btn.configure(state='disabled')
    
    def form_diagnosis(self):
        diagnosis = self.diagnosis_name.get()
        prescription = self.prescription_entry.get()
        if prescription and diagnosis:
            prescription_list = prescription.split(',')
            keys = []
            items = []
            for med in prescription_list:
                new_list = med.split(':')
                keys.append(new_list[0])
                items.append(new_list[1])
            prescription_dict = dict(zip(keys, items))
            self.appointment.form_diagnosis(diagnosis, prescription_dict)
            messagebox.showinfo('Prescrition details details', self.appointment.current_diagnosis)
        else:
            messagebox.showwarning('Not all data', 'No diagnosis or no Prescription')  

