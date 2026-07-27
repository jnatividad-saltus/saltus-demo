import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "data" / "saltus_demo.db"


def print_patient_records(conn):
    patients = conn.execute("SELECT patient_id, name FROM patients ORDER BY patient_id").fetchall()
    for patient_id, name in patients:
        print(f"\nPatient {patient_id}: {name}")
        for table_name in ["conditions", "encounters", "lab_results", "observations", "medications", "referrals"]:
            rows = conn.execute(
                f"SELECT * FROM {table_name} WHERE patient_id = ?",
                (patient_id,),
            ).fetchall()
            print(f"  {table_name}: {len(rows)} rows")
            if rows:
                for row in rows:
                    print(f"    {row}")


def run_patient_separation_test(conn):
    overall = []
    for table_name in ["conditions", "encounters", "lab_results", "observations", "medications", "referrals"]:
        rows = conn.execute(f"SELECT patient_id FROM {table_name}").fetchall()
        overall.extend(rows)

    existing_patient_ids = {row[0] for row in conn.execute("SELECT patient_id FROM patients").fetchall()}
    failures = []
    for patient_id in [row[0] for row in overall]:
        if patient_id not in existing_patient_ids:
            failures.append(patient_id)

    if failures:
        print("FAIL patient-separation: orphaned patient_id values found")
        print(failures)
        return False

    print("PASS patient-separation: all rows belong to existing patients")
    return True


def run_consistency_test(conn):
    failures = []
    patients = conn.execute("SELECT patient_id, family_physician_relationship_years FROM patients").fetchall()
    for patient_id, relationship_years in patients:
        earliest = conn.execute(
            "SELECT MIN(substr(date, 1, 4)) FROM encounters WHERE patient_id = ?",
            (patient_id,),
        ).fetchone()[0]
        if earliest is None:
            failures.append((patient_id, "no encounters"))
            continue
        earliest_year = int(earliest)
        expected_year = 2026 - relationship_years
        if earliest_year != expected_year:
            failures.append((patient_id, earliest_year, expected_year))

    if failures:
        print("FAIL consistency: earliest encounter year does not match relationship years")
        print(failures)
        return False

    print("PASS consistency: earliest encounter year matches relationship years")
    return True


def main():
    conn = sqlite3.connect(DB_PATH)
    print_patient_records(conn)
    patient_separation_ok = run_patient_separation_test(conn)
    consistency_ok = run_consistency_test(conn)
    conn.close()

    print("\nSummary")
    print(f"  patient-separation: {'PASS' if patient_separation_ok else 'FAIL'}")
    print(f"  consistency: {'PASS' if consistency_ok else 'FAIL'}")


if __name__ == "__main__":
    main()
