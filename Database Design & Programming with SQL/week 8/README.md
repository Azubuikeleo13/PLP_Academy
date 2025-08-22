# 🏥 Clinic Booking System (MySQL Project)

## 📋 Description

A complete MySQL-based Clinic Booking System that allows managing patients, doctors, appointments, prescriptions, and medications. Designed to demonstrate SQL normalization, constraints, and relationship handling.

---

## 📁 Features

- Patient registration
- Doctor management and specialization tracking
- Appointment scheduling
- Prescription and medication handling (many-to-many)

---

## 🚀 How to Run

### 1. Clone the repository:

```bash
  git clone https://github.com/yourusername/clinic-booking-system.git
  cd 'PLP_Academy/Database Design & Programming with SQL/week 8/'
```

### 2. Import SQL into MySQL:

```Using MySQL CLI:
  mysql -u youruser -p clinic_db < clinic_db_schema.sql
  Or import via phpMyAdmin or MySQL Workbench.
```

## ERD Diagram

+---------------------+          +--------------------+
|   Specializations   |          |     Medications    |
+---------------------+          +--------------------+
| id (PK)             |          | id (PK)            |
| name (UNIQUE)       |          | name               |
+---------------------+          | dosage             |
                                 +--------------------+
        ▲
        | FK
        |
+---------------------+          +----------------------+
|      Doctors        |          |     Prescriptions     |
+---------------------+          +----------------------+
| id (PK)             |          | id (PK)              |
| first_name          |          | appointment_id (FK)  |
| last_name           |          | notes                |
| email (UNIQUE)      |          +----------------------+
| specialization_id   |
+---------------------+                   ▲
        ▲                                  |
        |                                  |
        |                                  |
+---------------------+           +------------------------+
|    Appointments      |◄─────────| prescription_medications |
+---------------------+           +------------------------+
| id (PK)             |           | prescription_id (PK/FK) |
| doctor_id (FK)      |           | medication_id (PK/FK)   |
| patient_id (FK)     |           +------------------------+
| appointment_date    |
| reason              |        
+---------------------+
        ▲
        |
+---------------------+
|      Patients        |
+---------------------+
| id (PK)             |
| first_name          |
| last_name           |
| date_of_birth       |
| phone (UNIQUE)      |
| email (UNIQUE)      |
+---------------------+

## 📂 Contents

- clinic_db_schema.sql — Contains all CREATE TABLE statements with constraints and relationships.

- clinic_db_schema-mock_data.sql — Contains all INSERT statements with dummy data for each tables for Testing.

- README.md — This file.

## 📜 License

MIT License
