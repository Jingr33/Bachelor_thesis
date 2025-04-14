""" This script count items in each patient YOLO dataset folder and write results into txt file.
"""

import os


DATASET_PATH = "dataset4"

result_content = []
sum_count = 0
for patient_dir in os.listdir(DATASET_PATH):
    # skip partial datasets and non folders
    if "_" in patient_dir or "-" in patient_dir or "." in patient_dir:
        continue
    
    file_count = len(os.listdir(os.path.join(DATASET_PATH, patient_dir, "images")))
    sum_count += file_count
    result_content.append(f"{patient_dir} - {file_count}\n")

result_content.append(f"\nDATASET SUM: {sum_count}\n")
result_content.append(f"10% of dataset: {int(sum_count / 10)}\n")
result_content.append(f"20% of dataset: {int(sum_count / 5)}\n")

with open(os.path.join(DATASET_PATH, "patient_sizes.txt"), 'w', encoding='utf-8') as f:
    f.writelines(result_content)

print(f"Vytvořen soubor {os.path.join(DATASET_PATH, "patien_sizes.txt")}.")