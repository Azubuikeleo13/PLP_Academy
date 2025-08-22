-- Clinic Booking System SQL Schema
-- Author: Leo Azubuike
-- Date: 22/08/2025

-- Create Databes/Schema if it does not exist
CREATE DATABASE IF NOT EXISTS clinicB_db;

/* Switch to the clinicB_db database */
USE clinicB_db;

-- Drop tables if they exist (for development/testing purposes)
DROP TABLE IF EXISTS prescription_medications;
DROP TABLE IF EXISTS prescriptions;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS medications;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS specializations;

-- Table: Specializations
CREATE TABLE specializations (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE
);

-- Table: Doctors
CREATE TABLE doctors (
  id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  specialization_id INT,
  FOREIGN KEY (specialization_id) REFERENCES specializations(id)
);

-- Table: Patients
CREATE TABLE patients (
  id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  date_of_birth DATE NOT NULL,
  phone VARCHAR(20) UNIQUE,
  email VARCHAR(100) UNIQUE
);

-- Table: Appointments
CREATE TABLE appointments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  doctor_id INT NOT NULL,
  patient_id INT NOT NULL,
  appointment_date DATETIME NOT NULL,
  reason TEXT,
  FOREIGN KEY (doctor_id) REFERENCES doctors(id),
  FOREIGN KEY (patient_id) REFERENCES patients(id)
);

-- Table: Prescriptions
CREATE TABLE prescriptions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  appointment_id INT NOT NULL,
  notes TEXT,
  FOREIGN KEY (appointment_id) REFERENCES appointments(id)
);

-- Table: Medications
CREATE TABLE medications (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  dosage VARCHAR(50)
);

-- Join Table: prescription_medications (Many-to-Many)
CREATE TABLE prescription_medications (
  prescription_id INT NOT NULL,
  medication_id INT NOT NULL,
  PRIMARY KEY (prescription_id, medication_id),
  FOREIGN KEY (prescription_id) REFERENCES prescriptions(id),
  FOREIGN KEY (medication_id) REFERENCES medications(id)
);
