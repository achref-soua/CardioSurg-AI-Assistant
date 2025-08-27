import json
import os


def load_existing_data():
    """Load existing patients, devices, and notes data."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "../preprocessed_data")

    # Load devices to understand what we have
    with open(os.path.join(data_dir, "devices.json"), "r", encoding="utf-8") as f:
        devices = json.load(f)

    # Load patients to understand diagnoses
    with open(os.path.join(data_dir, "patients.json"), "r", encoding="utf-8") as f:
        patients = json.load(f)

    return devices, patients


def generate_guidelines(devices, patients):
    """Generate clinical practice guidelines based on existing devices and patient conditions."""

    # Extract unique diagnoses

    diagnoses = list(
        set(
            [
                patient.get("diagnosis", "")
                for patient in patients
                if patient.get("diagnosis")
            ]
        )
    )

    guidelines = []

    # Generate device-specific guidelines
    for i, device in enumerate(devices):
        device_name = device.get("device_name", f"Device {i + 1}")
        indication = device.get("indication", "General vascular intervention")
        manufacturer = device.get("manufacturer", "Unknown")

        # Pre-operative guidelines
        preop_guideline = {
            "doc_id": f"GUIDELINE-PREOP-{device.get('device_id', f'DEV{i + 1}')}",
            "section": "pre_operative_planning",
            "text": f"CLINICAL PRACTICE GUIDELINE: Pre-operative Planning for {device_name} ({indication})\n\n"
            f"Patient Selection Criteria:\n"
            f"- Confirmed diagnosis requiring {indication} intervention\n"
            f"- Appropriate anatomical requirements as per device specifications\n"
            f"- Absence of contraindications listed in device manual\n"
            f"- Patient fitness for endovascular procedure\n\n"
            f"Pre-operative Assessment:\n"
            f"- High-resolution CT angiography with contrast\n"
            f"- Assessment of access vessels (femoral/iliac arteries)\n"
            f"- Cardiac risk stratification\n"
            f"- Renal function evaluation\n"
            f"- Coagulation profile assessment\n\n"
            f"Sizing Requirements:\n"
            f"- Proximal landing zone assessment\n"
            f"- Distal landing zone evaluation\n"
            f"- Oversizing calculations as per manufacturer guidelines\n"
            f"- Alternative access route planning if needed",
            "source": f"{manufacturer} Clinical Guidelines 2024",
        }
        guidelines.append(preop_guideline)

        # Intra-operative guidelines
        intraop_guideline = {
            "doc_id": f"GUIDELINE-INTRAOP-{device.get('device_id', f'DEV{i + 1}')}",
            "section": "intra_operative_procedure",
            "text": f"CLINICAL PRACTICE GUIDELINE: Intra-operative Procedure for {device_name}\n\n"
            f"Equipment Preparation:\n"
            f"- Verify device size and specifications\n"
            f"- Prepare delivery system components\n"
            f"- Ensure fluoroscopy equipment calibration\n"
            f"- Prepare emergency bailout devices\n\n"
            f"Procedural Steps:\n"
            f"- Establish vascular access under ultrasound guidance\n"
            f"- Perform diagnostic angiography\n"
            f"- Deploy device according to manufacturer instructions\n"
            f"- Verify proper positioning and seal\n"
            f"- Perform completion angiography\n\n"
            f"Quality Control:\n"
            f"- Confirm absence of endoleaks\n"
            f"- Verify hemostasis at access sites\n"
            f"- Document procedural details thoroughly",
            "source": "Endovascular Surgery Guidelines 2024",
        }
        guidelines.append(intraop_guideline)

        # Post-operative guidelines
        postop_guideline = {
            "doc_id": f"GUIDELINE-POSTOP-{device.get('device_id', f'DEV{i + 1}')}",
            "section": "post_operative_care",
            "text": f"CLINICAL PRACTICE GUIDELINE: Post-operative Care for {device_name} Patients\n\n"
            f"Immediate Post-operative Care (0-24 hours):\n"
            f"- Hemodynamic monitoring\n"
            f"- Access site assessment for bleeding/hematoma\n"
            f"- Distal pulse examination\n"
            f"- Pain management protocol\n"
            f"- Early mobilization when appropriate\n\n"
            f"Discharge Planning:\n"
            f"- Patient education on warning signs\n"
            f"- Medication reconciliation\n"
            f"- Follow-up appointment scheduling\n"
            f"- Activity restrictions counseling\n\n"
            f"Long-term Surveillance:\n"
            f"- 30-day post-operative imaging\n"
            f"- Annual CT surveillance\n"
            f"- Clinical assessment every 6 months\n"
            f"- Endoleak monitoring protocol",
            "source": "Post-operative Care Guidelines 2024",
        }
        guidelines.append(postop_guideline)

    # Generate general condition-based guidelines
    for diagnosis in diagnoses:
        general_guideline = {
            "doc_id": f"GUIDELINE-GENERAL-{diagnosis.replace(' ', '_').replace('(', '').replace(')', '').upper()}",
            "section": "general_management",
            "text": f"CLINICAL PRACTICE GUIDELINE: Management of {diagnosis}\n\n"
            f"Definition and Classification:\n"
            f"{diagnosis} represents a significant cardiovascular condition requiring specialized management. "
            f"Treatment approach depends on anatomical characteristics, patient risk factors, and available expertise.\n\n"
            f"Treatment Indications:\n"
            f"- Size criteria meeting intervention thresholds\n"
            f"- Symptomatic presentation\n"
            f"- Rapid growth rate\n"
            f"- Patient life expectancy considerations\n\n"
            f"Treatment Options:\n"
            f"- Endovascular repair (preferred when anatomically suitable)\n"
            f"- Open surgical repair (for complex anatomy)\n"
            f"- Medical management for high-risk patients\n"
            f"- Hybrid procedures when indicated\n\n"
            f"Risk Assessment:\n"
            f"- Anatomical risk factors evaluation\n"
            f"- Cardiac risk stratification\n"
            f"- Pulmonary function assessment\n"
            f"- Renal function evaluation",
            "source": "Vascular Surgery Society Guidelines 2024",
        }
        guidelines.append(general_guideline)

    return guidelines


def generate_literature(devices, patients):
    """Generate research literature based on existing devices and patient conditions."""

    literature = []

    # Device-specific research articles
    for i, device in enumerate(devices):
        device_name = device.get("device_name", f"Device {i + 1}")
        indication = device.get("indication", "vascular intervention")
        manufacturer = device.get("manufacturer", "Medical Device Co.")

        # Clinical outcomes study
        outcomes_study = {
            "doc_id": f"LITERATURE-OUTCOMES-{device.get('device_id', f'DEV{i + 1}')}",
            "section": "clinical_outcomes_study",
            "text": f"Clinical Outcomes of {device_name} for {indication}: A Multi-Center Analysis\n\n"
            f"Background: The {device_name} by {manufacturer} represents an advancement in endovascular "
            f"treatment for {indication}. This study evaluates the clinical outcomes and safety profile "
            f"in a real-world patient population.\n\n"
            f"Methods: Retrospective analysis of 250 patients treated with {device_name} across 12 centers "
            f"over 24 months. Primary endpoints included technical success, 30-day mortality, and freedom "
            f"from reintervention at 1 year.\n\n"
            f"Results: Technical success was achieved in 96.8% of cases. The 30-day mortality rate was 1.2%, "
            f"with major complications occurring in 4.8% of patients. At 1-year follow-up, freedom from "
            f"reintervention was 94.2%. Type II endoleaks were observed in 12% of patients but showed "
            f"spontaneous resolution in 78% of cases.\n\n"
            f"Conclusions: The {device_name} demonstrates excellent technical success rates with low "
            f"morbidity and mortality. Long-term surveillance confirms durability of repair with minimal "
            f"reintervention requirements.",
            "source": "Journal of Endovascular Surgery 2024",
        }
        literature.append(outcomes_study)

        # Technical innovation study
        tech_study = {
            "doc_id": f"LITERATURE-TECH-{device.get('device_id', f'DEV{i + 1}')}",
            "section": "technical_innovation",
            "text": f"Technical Innovation in {device_name}: Design Features and Clinical Applications\n\n"
            f"Introduction: The evolution of endovascular devices continues to expand treatment options "
            f"for complex vascular pathology. The {device_name} incorporates novel design features "
            f"aimed at improving procedural outcomes and long-term durability.\n\n"
            f"Device Characteristics: The {device_name} features advanced delivery system technology "
            f"with enhanced flexibility and precision deployment mechanisms. Key design elements include "
            f"optimized radial force, conformability to vessel anatomy, and biocompatible materials.\n\n"
            f"Clinical Experience: Initial clinical experience demonstrates favorable handling characteristics "
            f"and deployment accuracy. The device shows excellent conformability to tortuous anatomy "
            f"while maintaining structural integrity. Deployment precision allows for accurate positioning "
            f"in challenging anatomical configurations.\n\n"
            f"Future Directions: Continued refinement of device technology focuses on expanding "
            f"anatomical applicability and improving long-term durability. Integration of advanced "
            f"imaging guidance systems may further enhance procedural outcomes.",
            "source": "Cardiovascular Engineering and Technology 2024",
        }
        literature.append(tech_study)

    # General research topics based on diagnoses
    diagnoses = list(
        set(
            [
                patient.get("diagnosis", "")
                for patient in patients
                if patient.get("diagnosis")
            ]
        )
    )

    for diagnosis in diagnoses:
        epidemiology_study = {
            "doc_id": f"LITERATURE-EPI-{diagnosis.replace(' ', '_').replace('(', '').replace(')', '').upper()}",
            "section": "epidemiology_study",
            "text": f"Epidemiology and Risk Factors of {diagnosis}: A Population-Based Analysis\n\n"
            f"Objective: To analyze the epidemiological trends and risk factor associations for {diagnosis} "
            f"in a large population-based cohort study.\n\n"
            f"Methods: Analysis of 50,000 patients from a national registry over 10 years. Risk factors, "
            f"demographics, and outcomes were analyzed using multivariate regression models.\n\n"
            f"Results: The incidence of {diagnosis} has increased by 15% over the study period, primarily "
            f"in patients over 65 years of age. Key risk factors include hypertension (OR 2.1), smoking "
            f"history (OR 1.8), hyperlipidemia (OR 1.6), and male gender (OR 2.3). Geographic variations "
            f"were observed with higher incidence in urban populations.\n\n"
            f"Screening and Prevention: Risk-based screening protocols show promise in early detection. "
            f"Lifestyle modifications and medical management of risk factors may reduce progression rates. "
            f"Population health initiatives targeting high-risk groups demonstrate cost-effectiveness.\n\n"
            f"Conclusions: Understanding epidemiological patterns enables targeted prevention strategies "
            f"and resource allocation. Early detection through screening programs may improve outcomes "
            f"and reduce healthcare costs.",
            "source": "Vascular Medicine Epidemiology 2024",
        }
        literature.append(epidemiology_study)

        treatment_comparison = {
            "doc_id": f"LITERATURE-COMPARE-{diagnosis.replace(' ', '_').replace('(', '').replace(')', '').upper()}",
            "section": "treatment_comparison",
            "text": f"Comparative Effectiveness of Treatment Modalities for {diagnosis}: Systematic Review and Meta-Analysis\n\n"
            f"Background: Multiple treatment options exist for {diagnosis}, including endovascular repair, "
            f"open surgical repair, and medical management. This systematic review compares outcomes "
            f"across treatment modalities.\n\n"
            f"Methods: Systematic search of major databases identified 45 studies including 12,500 patients. "
            f"Primary outcomes included mortality, morbidity, and quality of life measures. Network "
            f"meta-analysis was performed using random-effects models.\n\n"
            f"Results: Endovascular repair demonstrated lower 30-day mortality (1.4% vs 3.2%, p<0.01) "
            f"compared to open repair, with shorter hospital stays (3.2 vs 8.1 days) and faster recovery. "
            f"Long-term survival was comparable between approaches. Reintervention rates were higher "
            f"with endovascular approach (8.2% vs 4.1% at 5 years).\n\n"
            f"Patient Selection: Anatomical factors strongly influence treatment selection. Age and "
            f"comorbidity profiles guide individualized treatment decisions. Multidisciplinary team "
            f"approach optimizes patient outcomes.\n\n"
            f"Conclusions: Treatment selection should be individualized based on anatomical factors, "
            f"patient characteristics, and institutional expertise. Both approaches demonstrate "
            f"acceptable outcomes when appropriately applied.",
            "source": "Cochrane Database of Systematic Reviews 2024",
        }
        literature.append(treatment_comparison)

    return literature


def save_data(guidelines, literature, output_dir):
    """Save the generated guidelines and literature data."""

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save guidelines
    guidelines_path = os.path.join(output_dir, "guidelines.json")
    with open(guidelines_path, "w", encoding="utf-8") as f:
        json.dump(guidelines, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(guidelines)} guidelines and saved to {guidelines_path}")

    # Save literature
    literature_path = os.path.join(output_dir, "literature.json")
    with open(literature_path, "w", encoding="utf-8") as f:
        json.dump(literature, f, indent=2, ensure_ascii=False)
    print(
        f"Generated {len(literature)} literature entries and saved to {literature_path}"
    )


def main():
    """Main execution function."""
    print("Loading existing data...")
    devices, patients = load_existing_data()

    print(f"Found {len(devices)} devices and {len(patients)} patients")

    print("Generating guidelines...")
    guidelines = generate_guidelines(devices, patients)

    print("Generating literature...")
    literature = generate_literature(devices, patients)

    # Determine output directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "../preprocessed_data")

    print("Saving generated data...")
    save_data(guidelines, literature, output_dir)

    print("Data generation complete!")
    print(f"Guidelines generated: {len(guidelines)}")
    print(f"Literature entries generated: {len(literature)}")


if __name__ == "__main__":
    main()
