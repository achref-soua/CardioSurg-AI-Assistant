import random
import datetime
import json
import os


# Synthetic data generators
def random_date(start, end):
    return start + datetime.timedelta(days=random.randint(0, (end - start).days))


names = [
    "John Doe",
    "Mary Smith",
    "Ali Ben",
    "Emma Chen",
    "Carlos Martinez",
    "Sophie Dubois",
    "David Rossi",
    "Anna Müller",
    "Ahmed Hassan",
    "Fatima Zahra",
    "Liam Johnson",
    "Olivia Brown",
    "Noah Wilson",
    "Ava Thompson",
    "Isabella Garcia",
    "Ethan Lee",
    "Mia Lopez",
    "Lucas Kim",
    "Charlotte Davis",
    "Amir Khan",
]
sexes = ["Male", "Female"]
risk_factors_list = [
    "Hypertension",
    "Smoking",
    "Hyperlipidemia",
    "Diabetes Mellitus Type 2",
    "Obesity",
    "Chronic Kidney Disease",
    "Family history of aneurysm",
    "Sedentary lifestyle",
]
diagnoses = [
    "Abdominal Aortic Aneurysm (AAA)",
    "Thoracic Aortic Aneurysm (TAA)",
    "Ascending Aortic Aneurysm",
]
planned_interventions = {
    "Abdominal Aortic Aneurysm (AAA)": "Endovascular Aneurysm Repair (EVAR)",
    "Thoracic Aortic Aneurysm (TAA)": "Thoracic Endovascular Aortic Repair (TEVAR)",
    "Ascending Aortic Aneurysm": "Open surgical repair with graft replacement",
}
aneurysm_locations = {
    "Abdominal Aortic Aneurysm (AAA)": "Infrarenal aorta",
    "Thoracic Aortic Aneurysm (TAA)": "Descending thoracic aorta",
    "Ascending Aortic Aneurysm": "Ascending aorta",
}

# Generate synthetic patients and EHRs
ehr_records = []
notes_records = []

for i in range(50):
    name = random.choice(names)
    sex = random.choice(sexes)
    age = random.randint(55, 80)
    diagnosis = random.choice(diagnoses)
    aneurysm_diameter = round(random.uniform(4.5, 7.0), 1)
    scan_date = random_date(datetime.date(2023, 1, 1), datetime.date(2024, 1, 1))
    patient_id = f"P{i + 1:03d}"
    risk_factors = ", ".join(random.sample(risk_factors_list, random.randint(2, 4)))

    # EHR record
    ehr_record = {
        "patient_id": patient_id,
        "name": name,
        "age": age,
        "sex": sex,
        "risk_factors": risk_factors,
        "diagnosis": diagnosis,
        "aneurysm_diameter_cm": aneurysm_diameter,
        "aneurysm_location": aneurysm_locations[diagnosis],
        "ct_scan_date": scan_date.strftime("%Y-%m-%d"),
        "planned_intervention": planned_interventions[diagnosis],
    }

    # Generate the unified text field for vectorization
    ehr_record["text"] = (
        f"Patient ID: {ehr_record['patient_id']}. "
        f"Name: {ehr_record['name']}. "
        f"Age: {ehr_record['age']}. "
        f"Sex: {ehr_record['sex']}. "
        f"Risk Factors: {ehr_record['risk_factors']}. "
        f"Diagnosis: {ehr_record['diagnosis']}. "
        f"Aneurysm Diameter: {ehr_record['aneurysm_diameter_cm']} cm. "
        f"Location: {ehr_record['aneurysm_location']}. "
        f"Planned Intervention: {ehr_record['planned_intervention']}."
    )

    ehr_records.append(ehr_record)

    # Notes records: multiple per patient (pre-op, intra-op, post-op, follow-up)
    notes_records.extend(
        [
            {
                "note_id": f"N-{patient_id}-PRE",
                "patient_id": patient_id,
                "note_type": "Pre-op",
                "timestamp": scan_date.strftime("%Y-%m-%dT09:00:00Z"),
                "text": f"Patient presents with {diagnosis}. Relevant risk factors: {ehr_record['risk_factors']}. Planning {planned_interventions[diagnosis]}.",
            },
            {
                "note_id": f"N-{patient_id}-INTRA",
                "patient_id": patient_id,
                "note_type": "Intra-op",
                "timestamp": (scan_date + datetime.timedelta(days=7)).strftime(
                    "%Y-%m-%dT11:00:00Z"
                ),
                "text": f"Procedure: {planned_interventions[diagnosis]}. Estimated blood loss: {random.randint(200, 800)} mL. No immediate complications.",
            },
            {
                "note_id": f"N-{patient_id}-POST",
                "patient_id": patient_id,
                "note_type": "Post-op",
                "timestamp": (scan_date + datetime.timedelta(days=8)).strftime(
                    "%Y-%m-%dT10:00:00Z"
                ),
                "text": f"Patient stable post-op. Recommend follow-up imaging in {random.choice([1, 3, 6])} months.",
            },
            {
                "note_id": f"N-{patient_id}-FOLLOW",
                "patient_id": patient_id,
                "note_type": "Follow-up",
                "timestamp": (scan_date + datetime.timedelta(days=30)).strftime(
                    "%Y-%m-%dT10:00:00Z"
                ),
                "text": "Follow-up visit: patient recovering well. No signs of complications. Vitals stable. Continue medical management.",
            },
        ]
    )

# Get the directory of the current script
base_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(base_dir, "../preprocessed_data")
os.makedirs(output_dir, exist_ok=True)

ehr_file_path = os.path.join(output_dir, "patients.json")
notes_file_path = os.path.join(output_dir, "notes.json")

with open(ehr_file_path, "w") as f:
    json.dump(ehr_records, f, indent=2)

with open(notes_file_path, "w") as f:
    json.dump(notes_records, f, indent=2)

print(f"EHR data saved to: {ehr_file_path}")
print(f"Notes data saved to: {notes_file_path}")
