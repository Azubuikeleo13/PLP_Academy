-- Mock Data Inserts for Clinic Booking System

-- Specializations
INSERT INTO specializations (name) VALUES 
('General Practitioner'),
('Dermatology'),
('Cardiology'),
('Neurology');

-- Doctors
INSERT INTO doctors (first_name, last_name, email, specialization_id) VALUES 
('Alice', 'Morgan', 'alice.morgan@clinic.com', 1),
('Bob', 'Smith', 'bob.smith@clinic.com', 2),
('Carla', 'Jones', 'carla.jones@clinic.com', 3);

-- Patients
INSERT INTO patients (first_name, last_name, date_of_birth, phone, email) VALUES 
('John', 'Doe', '1985-07-20', '1234567890', 'john.doe@gmail.com'),
('Jane', 'Smith', '1992-03-14', '2345678901', 'jane.smith@yahoo.com'),
('Emily', 'Clark', '2000-10-05', '3456789012', 'emily.clark@hotmail.com');

-- Appointments
INSERT INTO appointments (doctor_id, patient_id, appointment_date, reason) VALUES 
(1, 1, '2025-08-20 10:30:00', 'General Checkup'),
(2, 2, '2025-08-21 14:00:00', 'Skin Rash'),
(3, 3, '2025-08-22 09:15:00', 'Heart Palpitations');

-- Prescriptions
INSERT INTO prescriptions (appointment_id, notes) VALUES 
(1, 'Prescribed vitamins and recommended rest.'),
(2, 'Applied topical cream for rash.'),
(3, 'Referred to cardiologist for ECG.');

-- Medications
INSERT INTO medications (name, dosage) VALUES 
('Vitamin D3', '1000 IU'),
('Hydrocortisone Cream', '2%'),
('Aspirin', '81mg');

-- prescription_medications (Many-to-Many)
INSERT INTO prescription_medications (prescription_id, medication_id) VALUES 
(1, 1), -- Vitamin D3 for John
(2, 2), -- Cream for Jane
(3, 3); -- Aspirin for Emily
