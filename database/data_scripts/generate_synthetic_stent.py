import random
import json
import os

# synthetic manufacturers and device name patterns
manufacturers = [
    "Medivasc Technologies",
    "EndoLife Systems",
    "NeoGraft Medical",
    "FlowSecure Devices",
    "Aneurysafe Corp",
    "CardioVasc Solutions",
]
device_prefixes = [
    "Aneurysafe",
    "EndoFlex",
    "NeoSeal",
    "FlowGuard",
    "VascuShield",
    "StentSecure",
]
device_suffixes = ["Flex", "Pro", "Advance", "Elite", "Ultra", "Prime"]


# function to generate synthetic device record
def generate_device(device_id):
    manufacturer = random.choice(manufacturers)
    device_name = f"{random.choice(device_prefixes)} {random.randint(20, 40)} {random.choice(device_suffixes)}"
    indication = random.choice(
        ["Infrarenal AAA", "Juxtarenal AAA", "Thoracic Aneurysm", "Iliac Aneurysm"]
    )

    proximal_diam = sorted(random.sample(range(18, 40), 2))
    distal_diam = sorted(random.sample(range(10, 24), 2))
    length_options = sorted(random.sample(range(80, 200, 10), 3))

    anatomical_requirements = {
        "min_neck_length_mm": random.choice([10, 12, 15, 20, 25]),
        "max_neck_angulation_deg": random.choice([45, 50, 60, 70, 75]),
        "iliac_access_min_mm": random.choice([6, 7, 8]),
        "iliac_access_max_mm": random.choice([12, 14, 16]),
    }

    contraindications = []
    if anatomical_requirements["max_neck_angulation_deg"] < 70:
        contraindications.append(
            f"Neck angulation > {anatomical_requirements['max_neck_angulation_deg']}°"
        )
    contraindications.append(
        f"Neck length < {anatomical_requirements['min_neck_length_mm']} mm"
    )
    contraindications.append("Active infection at implant site")

    delivery_system = {
        "sheath_size_fr": random.choice([16, 18, 20, 22]),
        "flexibility": random.choice(["Low", "Medium", "High"]),
    }

    deployment_steps = [
        "Insert sheath via femoral access",
        "Advance stent graft under fluoroscopy",
        "Align proximal markers with renal arteries",
        "Deploy main body in controlled release",
        "Deploy contralateral limb",
        "Post-dilation with balloon catheter",
    ]

    device_record = {
        "device_id": f"SG-{device_id:04d}",
        "manufacturer": manufacturer,
        "device_name": device_name,
        "indication": indication,
        "sizing": {
            "proximal_diameter_range_mm": proximal_diam,
            "distal_diameter_range_mm": distal_diam,
            "length_options_mm": length_options,
        },
        "anatomical_requirements": anatomical_requirements,
        "contraindications": contraindications,
        "delivery_system": delivery_system,
        "deployment_steps": deployment_steps,
    }

    # Generate the unified text field for vectorization
    device_record["text"] = (
        f"Device ID: {device_record['device_id']}. "
        f"Manufacturer: {device_record['manufacturer']}. "
        f"Device Name: {device_record['device_name']}. "
        f"Indication: {device_record['indication']}. "
        f"Sizing: Proximal Diameter: {proximal_diam} mm, Distal Diameter: {distal_diam} mm, Length Options: {length_options} mm. "
        f"Anatomical Requirements: Min Neck Length: {anatomical_requirements['min_neck_length_mm']} mm, "
        f"Max Neck Angulation: {anatomical_requirements['max_neck_angulation_deg']} deg, "
        f"Iliac Access: {anatomical_requirements['iliac_access_min_mm']}-{anatomical_requirements['iliac_access_max_mm']} mm. "
        f"Contraindications: {', '.join(device_record['contraindications'])}. "
        f"Delivery System: Sheath Size: {delivery_system['sheath_size_fr']} Fr, Flexibility: {delivery_system['flexibility']}. "
        f"Deployment Steps: {', '.join(device_record['deployment_steps'])}."
    )

    return device_record


# generate 500 devices
synthetic_devices = [generate_device(i) for i in range(1, 501)]

# save to JSON
base_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(base_dir, "../preprocessed_data")
os.makedirs(output_dir, exist_ok=True)
file_path = os.path.join(output_dir, "devices.json")
with open(file_path, "w") as f:
    json.dump(synthetic_devices, f, indent=2)

print(f"Device data saved to: {file_path}")
