import os
import csv

# add patch names and severity label to dictionary for additional training
patient_severity = {
    "patient1_patch1": 1,
    "patient3_patch1": 0,
    "patient3_patch2": 0,
    "patient3_patch3": 0,
    "patient3_patch7": 0,
    "patient4_patch1": 1,
    "patient4_patch8": 1,
    "patient8_patch1": 1,
    "patient10_patch1": 1,
    "patient10_patch10": 1,
    "patient11_patch3": 1,
    "patient11_patch5": 1,
    "patient12_patch2": 1,
    "patient12_patch4": 1,
    "patient13_patch1": 0
}

output_file = "severity_labels.csv"
with open(output_file, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["patch_grouping", "severity"])
    writer.writeheader()
    for patch_grouping, severity in patient_severity.items():
        writer.writerow({"patch_grouping": patch_grouping, "severity": severity})

print(f"Severity labels saved to {output_file}")

