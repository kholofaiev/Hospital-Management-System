import tkinter as tk
from tkinter import messagebox, ttk
import asyncio
from datetime import date, datetime, timedelta
from Library.Hospital import Patient, Doctor


class PatientScreen(tk.Toplevel):
    def __init__(self,patient:Patient, doctors) -> None:
        super().__init__()
        self.title('Profile')
        self.geometry("450x600")
        self.doctors = doctors
        
        self.patient = patient
        
        self.profile = ProfileInfo(self, self.patient)
        self.profile.pack(fill="x", padx=10, pady=10)
        
        self.booking = BookingMenu(self, self.doctors, self.patient)
        self.booking.pack(fill="x", padx=10, pady=10)

class ProfileInfo(tk.LabelFrame):
    def __init__(self, parent, patient:Patient):
        super().__init__(parent, text="Profile")
        self.patient = patient
        
        tk.Label(self, text="Full Name:").grid(row=0, column=0, sticky="we", pady=10)
        self.name_var = tk.StringVar(value=self.patient.name)
        tk.Entry(self, textvariable=self.name_var).grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(self, text="DOB (YYYY-MM-DD):").grid(row=1, column=0, sticky="we", pady=10)
        self.dob_var = tk.StringVar(value=str(self.patient.birth_date))
        tk.Entry(self, textvariable=self.dob_var).grid(row=1, column=1, pady=2)
        
        tk.Button(self, text="Update Profile", command=self.update_profile).grid(row=2, column=0, columnspan=2, pady=10)
        
    def update_profile(self):
        try:
            self.patient.name = self.name_var.get()
            self.patient.birth_date = self.dob_var.get()
            
            self.name_var.set(self.patient.name)
            self.dob_var.set(str(self.patient.birth_date))
            messagebox.showinfo("Success", "Profile updated.")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")


class BookingMenu(tk.LabelFrame):
    def __init__(self,parent, doctors, patient:Patient):
        super().__init__(parent, text='Book Appointment')
        tk.Label(self, text="Select Doctor").pack()
        self.patient = patient
        self.doctors = doctors
        self.doctor_selector = ttk.Combobox(
            self,
            values=[f"Dr. {d.name} {d.specialty}" for d in self.doctors],
            state="readonly"
        )
        self.doctor_selector.current(0) 
        self.doctor_selector.pack(pady=5)
        
        self.date_entry = tk.Entry(self)
        self.date_entry.insert(0, str(date.today()))
        
        self.time_entry = tk.Entry(self)
        next_book = datetime.now().hour+1
        if next_book < 10:
            next_book = '10:00'
        elif next_book >15:
            next_book = '10:00'
            self.date_entry.delete(0)
            self.date_entry.delete(0,tk.END)
            self.date_entry.insert(0, str(date.today()+timedelta(1)))
        else:
            next_book = f'{next_book}:00'
        self.time_entry.insert(0, str(next_book))
        tk.Label(self, text="Enter Date YYYY-MM-DD").pack()
        self.date_entry.pack()
        tk.Label(self, text="Enter time HH:MM").pack()
        self.time_entry.pack()

        self.book_btn = tk.Button(self, text="Book Appointment", command=self.book)
        self.book_btn.pack(pady=10)
        self.history = tk.Listbox(self, width=60, height=8)
        for i in range(len(self.patient._history)):
            self.history.insert(i, self.patient._history[i])
        self.history.pack(padx=10, pady=5)
    
    
    def book(self):
        doctor = self.doctors[self.doctor_selector.current()]
        date = self.date_entry.get()
        time = self.time_entry.get()
        self.book_btn.config(state="active")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Using the doctor object selected from the list
            loop.run_until_complete(self.patient.create_appointment(doctor, date, time))
            self.after(0, self.booking_complete)
        except Exception as e:
            error_msg = str(e)
            self.after(0, lambda: messagebox.showerror("Error", error_msg))
            self.after(0, lambda: self.book_btn.config(state="normal"))
    
    def booking_complete(self):
        messagebox.showinfo('Success!', "Booking has been made")
        self.book_btn.config(state='normal')
        self.history.delete(0, tk.END)
        for appt in self.patient.get_history():
            self.history.insert(tk.END, str(appt))
        

          
if __name__ == "__main__":
    app = PatientScreen(Patient('John Doe', '1990-10-10'), doctors=[Doctor('James Fox', 'GP')])
    app.mainloop()