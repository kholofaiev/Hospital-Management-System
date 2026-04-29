import tkinter as tk
from tkinter import ttk
from Library.Hospital import Patient, Doctor 
from GUI.PatientGUI import PatientScreen
from GUI.DoctorGUI import DoctorDashboard

class Launcher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hospital")
        self.geometry("300x200")
        self.patients = [
            Patient('John Doe', '1999-01-01'),
            Patient('Jane Shepard', '2007-11-20')
        ]
        self.doctors = [
            Doctor('James Fox', 'GP'),
            Doctor('Michael Collins', 'Surgery')
        ]
        
        
        tk.Label(self,text='Choose Profile', font=("Arial", 12, "bold")).pack(pady=20)
        
        self.patien_select = ttk.Combobox(
            self,
            values=[p.name for p in self.patients],
            state="readonly"
        )
        self.patien_select.current(0)
        self.patien_btn = tk.Button(self, text="Patient", command=self.select_patient)
        self.patien_select.pack(pady=5, padx=10)
        self.patien_btn.pack(pady=5, padx=10)
        
        self.doctor_select = ttk.Combobox(
            self,
            values=[f'Dr. {d.name}' for d in self.doctors],
            state="readonly"
        )
        self.doctor_select.current(0)
        self.doctor_btn = tk.Button(self, text="Doctor", command=self.select_doctor)
        self.doctor_select.pack(pady=5, padx=10)
        self.doctor_btn.pack(pady=5, padx=10)
        
        
    def select_doctor(self):
        doctor_window = DoctorDashboard(self.doctors[self.doctor_select.current()], self.patients)
        self.withdraw()
        doctor_window.protocol("WM_DELETE_WINDOW", lambda: self.on_close_child(doctor_window))
    
    def select_patient(self):
        patient_window = PatientScreen(self.patients[self.patien_select.current()], self.doctors)
        self.withdraw()
        patient_window.protocol("WM_DELETE_WINDOW", lambda: self.on_close_child(patient_window))
    
    def on_close_child(self, child_window):
        child_window.destroy()
        self.deiconify() 
        
        
if __name__ == "__main__":
    app = Launcher()
    app.mainloop()