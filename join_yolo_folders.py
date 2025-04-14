""" This script join  more YOLO dataset forders with images and labels into one folder."""

import os
import sys
sys.path.append(r"C:\\Users\\ingrj\\AppData\\Roaming\\Python\\Python312\\site-packages")
import shutil


SOURCE_PATHS = (r"future_dataset/vid19_man",
                r"future_dataset/vid19_corr",
                r"future_dataset/vid19_auto")
TARGET_PATH = r"future_dataset/vid19"
SUBDIRS = ["images", "labels"]

for subdir in SUBDIRS:
    os.makedirs(os.path.join(TARGET_PATH, subdir), exist_ok=True)

def _next_available_id() -> int:
    """Find a first available id for a txt and jpg file names in the dataset."""
    highest_num = 0
    directory = os.path.join(TARGET_PATH, SUBDIRS[0])
    for file_name in os.listdir(directory):
        num = file_name.split(".")[0]
        if num.isdigit():
            highest_num = max(highest_num, int(num))
    return int(highest_num) + 1

for source_path in SOURCE_PATHS:
    FIRST_ID = _next_available_id()
    IDX = 0
    for file in os.listdir(os.path.join(source_path, SUBDIRS[0])):
        img_from = os.path.join(source_path, SUBDIRS[0], file)
        img_to = os.path.join(TARGET_PATH, SUBDIRS[0], f"{FIRST_ID + IDX}.{file.split(".")[1]}")
        shutil.copy2(img_from, img_to)

        annot_from = os.path.join(source_path, SUBDIRS[1], f"{file.split(".")[0]}.txt")
        annot_to = os.path.join(TARGET_PATH, SUBDIRS[1], f"{FIRST_ID + IDX}.txt")
        if os.path.exists(annot_from):
            shutil.copy2(annot_from, annot_to)

        IDX += 1
    print(f"Soubory z {source_path} zkopírovány do {TARGET_PATH}")

print("PŘESUN DOKONČEN!")
