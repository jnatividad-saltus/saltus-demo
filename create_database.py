import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "data" / "saltus_demo.db"


def create_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    conn.executescript(
        """
        CREATE TABLE patients (
            patient_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            sex TEXT NOT NULL,
            family_physician_relationship_years INTEGER NOT NULL,
            is_fictional TEXT NOT NULL DEFAULT 'yes'
        );

        CREATE TABLE conditions (
            condition_id INTEGER PRIMARY KEY,
            patient_id INTEGER NOT NULL REFERENCES patients(patient_id),
            condition_name TEXT NOT NULL,
            date_recorded TEXT NOT NULL,
            status TEXT NOT NULL
        );

        CREATE TABLE encounters (
            encounter_id INTEGER PRIMARY KEY,
            patient_id INTEGER NOT NULL REFERENCES patients(patient_id),
            date TEXT NOT NULL,
            encounter_type TEXT NOT NULL,
            note_text TEXT NOT NULL
        );

        CREATE TABLE lab_results (
            lab_id INTEGER PRIMARY KEY,
            patient_id INTEGER NOT NULL REFERENCES patients(patient_id),
            date TEXT NOT NULL,
            test_name TEXT NOT NULL,
            value REAL NOT NULL,
            unit TEXT NOT NULL
        );

        CREATE TABLE observations (
            obs_id INTEGER PRIMARY KEY,
            patient_id INTEGER NOT NULL REFERENCES patients(patient_id),
            date TEXT NOT NULL,
            observation_type TEXT NOT NULL,
            value TEXT NOT NULL,
            unit TEXT NOT NULL
        );

        CREATE TABLE medications (
            med_id INTEGER PRIMARY KEY,
            patient_id INTEGER NOT NULL REFERENCES patients(patient_id),
            medication_name TEXT NOT NULL,
            dose TEXT NOT NULL,
            date_started TEXT NOT NULL,
            date_stopped TEXT,
            notes TEXT
        );

        CREATE TABLE referrals (
            referral_id INTEGER PRIMARY KEY,
            patient_id INTEGER NOT NULL REFERENCES patients(patient_id),
            date TEXT NOT NULL,
            specialty TEXT NOT NULL,
            status TEXT NOT NULL,
            notes TEXT
        );
        """
    )

    patients = [
        (1, "Michael Thompson", 42, "male", 10, "yes"),
        (2, "Sarah Chen", 68, "female", 25, "yes"),
        (3, "Robert Singh", 55, "male", 5, "yes"),
    ]
    conn.executemany(
        "INSERT INTO patients (patient_id, name, age, sex, family_physician_relationship_years, is_fictional) VALUES (?, ?, ?, ?, ?, ?)",
        patients,
    )

    conditions = [
        (1, 1, "Type 2 diabetes", "2023-05-18", "active"),
        (2, 1, "Hypertension", "2021-03-08", "active"),
        (3, 1, "Hyperlipidemia", "2022-04-12", "active"),
        (4, 2, "Type 2 diabetes", "2005-04-20", "active"),
        (5, 2, "CKD Stage 3", "2020-02-03", "active"),
        (6, 3, "Type 2 diabetes", "2021-02-12", "active"),
        (7, 3, "Hypertension", "2021-02-12", "active"),
        (8, 3, "Heart failure", "2023-01-18", "active"),
    ]
    conn.executemany(
        "INSERT INTO conditions (condition_id, patient_id, condition_name, date_recorded, status) VALUES (?, ?, ?, ?, ?)",
        conditions,
    )

    encounters = [
        (1, 1, "2016-01-15", "initial visit", "Baseline visit; healthy at entry."),
        (2, 1, "2019-04-10", "follow-up", "Prediabetes documented after labs."),
        (3, 1, "2021-03-08", "follow-up", "Hypertension recorded after persistent elevated blood pressure."),
        (4, 1, "2022-04-12", "follow-up", "Hyperlipidemia documented and statin started."),
        (5, 1, "2023-05-18", "follow-up", "Type 2 diabetes diagnosed and metformin started."),
        (6, 1, "2024-08-20", "follow-up", "Catch-up visit after a gap; labs redrawn; metformin increased to 1000 mg twice daily."),
        (7, 1, "2025-02-14", "annual review", "Annual review with stable results."),
        (8, 2, "2001-01-12", "initial visit", "Joined practice at age 43."),
        (9, 2, "2005-04-20", "follow-up", "Type 2 diabetes diagnosed and metformin started."),
        (10, 2, "2012-06-08", "chronic care", "Representative chronic care visit."),
        (11, 2, "2016-09-10", "follow-up", "Diabetes review with HbA1c drifting."),
        (12, 2, "2019-11-14", "follow-up", "Labs showed declining eGFR and kidney concern noted."),
        (13, 2, "2020-02-03", "follow-up", "CKD Stage 3 documented, nephrology referral sent, nephrology consult completed, and letter received."),
        (14, 2, "2022-03-18", "follow-up", "Primary care note references a nephrology suggested recheck interval."),
        (15, 2, "2023-03-05", "annual review", "Annual review with nephrology follow-up letter received."),
        (16, 2, "2025-01-20", "annual review", "Labs stable; nephrology letter received and filed."),
        (17, 3, "2021-02-12", "transfer note", "Transferred in with established type 2 diabetes and hypertension."),
        (18, 3, "2021-06-22", "medication reconciliation", "Medication reconciliation completed after transfer."),
        (19, 3, "2022-04-14", "follow-up", "Routine follow-up with blood pressure review."),
        (20, 3, "2022-10-05", "follow-up", "Exertional breathlessness reported and investigations arranged."),
        (21, 3, "2023-01-18", "follow-up", "Heart failure documented and cardiology referral sent."),
        (22, 3, "2023-06-14", "specialist letter received", "Cardiology consult letter received and medications adjusted."),
        (23, 3, "2024-10-18", "phone encounter", "Patient called regarding hydrochlorothiazide; advised to stop; will confirm medication list at next visit."),
    ]
    conn.executemany(
        "INSERT INTO encounters (encounter_id, patient_id, date, encounter_type, note_text) VALUES (?, ?, ?, ?, ?)",
        encounters,
    )

    lab_results = [
        (1, 1, "2019-04-10", "HbA1c", 6.2, "%"),
        (2, 1, "2023-05-18", "HbA1c", 7.9, "%"),
        (3, 1, "2024-08-20", "HbA1c", 7.2, "%"),
        (4, 1, "2025-02-14", "HbA1c", 6.8, "%"),
        (5, 1, "2024-08-20", "LDL", 118.0, "mg/dL"),
        (6, 2, "2016-09-10", "HbA1c", 7.5, "%"),
        (7, 2, "2019-11-14", "eGFR", 58.0, "mL/min/1.73m2"),
        (8, 2, "2022-06-15", "HbA1c", 7.3, "%"),
        (9, 2, "2023-03-05", "eGFR", 50.0, "mL/min/1.73m2"),
        (10, 2, "2024-04-22", "HbA1c", 7.1, "%"),
        (11, 2, "2025-01-20", "eGFR", 48.0, "mL/min/1.73m2"),
        (12, 2, "2024-04-22", "urine albumin-to-creatinine ratio", 18.0, "mg/g"),
        (13, 3, "2021-02-12", "HbA1c", 8.1, "%"),
        (14, 3, "2023-01-18", "natriuretic peptide", 320.0, "pg/mL"),
        (15, 3, "2023-06-14", "creatinine", 1.3, "mg/dL"),
        (16, 3, "2024-10-18", "HbA1c", 7.4, "%"),
        (17, 3, "2025-03-10", "HbA1c", 7.5, "%"),
    ]
    conn.executemany(
        "INSERT INTO lab_results (lab_id, patient_id, date, test_name, value, unit) VALUES (?, ?, ?, ?, ?, ?)",
        lab_results,
    )

    observations = [
        (1, 1, "2016-01-15", "weight", "82.0", "kg"),
        (2, 1, "2019-04-10", "weight", "90.0", "kg"),
        (3, 1, "2021-03-08", "blood pressure", "148/92", "mmHg"),
        (4, 2, "2020-02-03", "blood pressure", "138/84", "mmHg"),
        (5, 2, "2022-06-08", "weight", "74.0", "kg"),
        (6, 2, "2024-04-22", "blood pressure", "136/82", "mmHg"),
        (7, 3, "2023-01-18", "weight", "92.0", "kg"),
        (8, 3, "2024-10-18", "weight", "96.0", "kg"),
        (9, 3, "2025-03-02", "weight", "99.0", "kg"),
        (10, 3, "2022-04-14", "blood pressure", "142/88", "mmHg"),
    ]
    conn.executemany(
        "INSERT INTO observations (obs_id, patient_id, date, observation_type, value, unit) VALUES (?, ?, ?, ?, ?, ?)",
        observations,
    )

    medications = [
        (1, 1, "metformin", "500 mg twice daily", "2023-05-18", None, "Medication listed on current regimen."),
        (2, 1, "lisinopril", "10 mg daily", "2021-03-08", None, "Medication listed on current regimen."),
        (3, 1, "atorvastatin", "20 mg nightly", "2022-04-12", None, "Medication listed on current regimen."),
        (4, 2, "metformin", "500 mg daily", "2005-04-20", None, "Active; renal dosing context noted."),
        (5, 2, "glipizide", "5 mg daily", "2012-06-08", None, "Medication listed on current regimen."),
        (6, 2, "lisinopril", "10 mg daily", "2016-09-10", None, "Medication listed on current regimen."),
        (7, 2, "furosemide", "40 mg daily", "2020-02-03", None, "Documented by nephrology for volume management."),
        (8, 3, "metformin", "500 mg twice daily", "2021-02-12", None, "Medication listed on current regimen."),
        (9, 3, "lisinopril", "10 mg daily", "2021-02-12", "2023-06-14", "Stopped when valsartan was recorded after cardiology review."),
        (10, 3, "metoprolol", "25 mg daily", "2023-01-18", None, "Medication listed on current regimen."),
        (11, 3, "furosemide", "40 mg daily", "2023-01-18", None, "Medication listed on current regimen."),
        (12, 3, "atorvastatin", "20 mg nightly", "2021-06-22", None, "Medication listed on current regimen."),
        (13, 3, "hydrochlorothiazide", "25 mg daily", "2021-06-22", None, "Started 2021 for blood pressure."),
        (14, 3, "valsartan", "80 mg daily", "2023-06-14", None, "Medication listed on current regimen."),
    ]
    conn.executemany(
        "INSERT INTO medications (med_id, patient_id, medication_name, dose, date_started, date_stopped, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
        medications,
    )

    referrals = [
        (1, 2, "2020-02-03", "nephrology", "sent", "Nephrology referral sent for kidney concern."),
        (2, 2, "2020-03-12", "nephrology", "completed", "Nephrology consult completed and letter received."),
        (3, 2, "2025-01-20", "nephrology", "filed", "Follow-up letter received and filed."),
        (4, 3, "2023-01-18", "cardiology", "sent", "Cardiology referral sent after heart failure documentation."),
        (5, 3, "2023-06-14", "cardiology", "completed", "Cardiology follow-up letter received."),
    ]
    conn.executemany(
        "INSERT INTO referrals (referral_id, patient_id, date, specialty, status, notes) VALUES (?, ?, ?, ?, ?, ?)",
        referrals,
    )

    conn.commit()

    row_counts = {}
    for table_name in ["patients", "conditions", "encounters", "lab_results", "observations", "medications", "referrals"]:
        count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        row_counts[table_name] = count

    expected = {
        "patients": 3,
        "conditions": 8,
        "encounters": 23,
        "lab_results": 17,
        "observations": 10,
        "medications": 14,
        "referrals": 5,
    }

    if row_counts != expected:
        raise ValueError(f"Unexpected row counts: {row_counts}")

    conn.close()
    print(f"Created {DB_PATH} with row counts: {row_counts}")


if __name__ == "__main__":
    create_database()
