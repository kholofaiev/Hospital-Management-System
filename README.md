# Hospital Management System
Hospital Management & Appointment System
> A comprehensive Python-based hospital management ecosystem featuring Object-Oriented domain modeling, asynchronous scheduling, a FastAPI REST service, a Flask web application, and a Tkinter desktop GUI.

## 📌 Overview

This project simulates hospital administration workflows such as patient-doctor interactions, appointment scheduling, and prescription/diagnosis management. Built as a multi-tier Python application, it demonstrates software engineering principles across pure OOP, desktop UI, asynchronous concurrency, and web services.

---

## ✨ Key Features

* **Core Domain Modeling:**
  * Object-Oriented classes for `Patient`, `Doctor`, `Appointment`, `Diagnosis`, and `Prescription`.
  * Asynchronous slot booking using Python's `asyncio.Lock` to prevent double-booking race conditions.
* **RESTful API (FastAPI):**
  * JWT (Bearer) authentication and user registration logic.
  * Role-based checks distinguishing patient and doctor workflows.
  * Appointment booking, retrieval, and status updates via SQLAlchemy ORM.
* **Web Interface (Flask):**
  * Server-side rendered interface with session-based authentication and hashed password handling via Werkzeug.
  * Dynamic dashboards allowing patients to book appointments and doctors to update diagnoses/prescriptions.
* **Desktop GUI (Tkinter):**
  * Desktop interface enabling profile switching between patients and doctors.

---

## 🛠️ Tech Stack

* **Language:** Python 3.9+
* **Web & API Frameworks:** FastAPI, Flask
* **Database & ORM:** SQLAlchemy, SQLite
* **Authentication:** OAuth2 (JWT Tokens), Werkzeug Security
* **Desktop GUI:** Tkinter / `ttk`
* **Concurrency:** `asyncio`

---

## 🎓 Academic Context

**Course:** Programming technologies

**Topics Covered:** Object-Oriented Programming (OOP), Asynchronous Programming, Web Frameworks, Database ORM, GUI Development.
