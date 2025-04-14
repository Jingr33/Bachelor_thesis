""" This code converts json file with images and its annotations in YOLO DATASET format. 
"""

import os
import sys
import json
import base64
from io import BytesIO
import importlib
sys.path.append(r"C:\\Users\\ingrj\\AppData\\Roaming\\Python\\Python312\\site-packages")
from PIL import Image


JSON_FILE = "C:/bakalarka/jsons/vid20c.json" # a source json file name
TARGET_DIR = "C:/bakalarka/future_dataset/vid20_corr" # target path to directory with YOLO dataset
POLYGON_ANNOTS = True # true if annotation type of images is polygonal, false if rectangular
    # -> if true, change folder in polygons2rectangles.py

PACIENT_SUBDIRS = ["images", "labels"]

def _mkdir_dataset() -> int:
    """Prepare tree structure of folders for YOLO dataset of one paTient.
    
    Return:
        int: next avalaible index in dataset folder, if new folder is created, return next_id = 0
    """
    for subdir in PACIENT_SUBDIRS:
        path = os.path.join(TARGET_DIR, subdir)
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok = True)

def _next_available_id() -> int:
    """Find a first available id for a txt and jpg file names in the dataset."""
    highest_num = 0
    directory = os.path.join(TARGET_DIR, PACIENT_SUBDIRS[0])
    for file_name in os.listdir(directory):
        num = file_name.split(".")[0]
        if num.isdigit():
            highest_num = max(highest_num, int(num))
    return int(highest_num) + 1

def _save_images(contents, first_id : int) -> None:
    """Save an image into the images folder."""
    for image in contents["images"]:
        image_data = base64.b64decode(image["file_name"].replace("data:image/jpg;base64,", ""))
        image_name = f"{image["id"] + first_id}.jpg"
        image = Image.open(BytesIO(image_data))
        image.save(os.path.join(TARGET_DIR, PACIENT_SUBDIRS[0], image_name))

def _create_annot_files(contents, first_id : int) -> None:
    """Save an annotations into the labels folder in YOLO format."""
    for annot in contents["annotations"]:
        # create annotation.txt file name
        annot_name = f"{annot["image_id"] + first_id}.txt"
        annot_path = os.path.join(TARGET_DIR, PACIENT_SUBDIRS[1], annot_name)
        ## annotation file content
        annot_category = str(annot["category_id"])
        coords_list = _normalize_coords(contents, annot)
        annot_coords = str(coords_list).replace(",", "").replace("[", "").replace("]", "")
        file_line = f"{annot_category} {annot_coords}\n"

        with open (annot_path, "a", encoding='utf-8') as f:
            f.write(file_line)

def _normalize_coords(contents, annot) -> list:
    """ Method for normalization of annotation coordinates."""
    image = next((item for item in contents["images"] if item["id"] == annot["image_id"]), None)
    width = image["width"]
    height = image["height"]
    for i in range(len(annot["segmentation"][0])):
        if i % 2 == 0:
            annot["segmentation"][0][i] = annot["segmentation"][0][i] / width
        else:
            annot["segmentation"][0][i] = annot["segmentation"][0][i] / height
    return annot["segmentation"]

with open(JSON_FILE, 'r', encoding='utf-8') as j:
    jsons_content = json.loads(j.read())

print(f"Vytvářím dataset ve složce {TARGET_DIR}...")
_mkdir_dataset()
AVAILABLE_ID = _next_available_id()
_save_images(jsons_content, AVAILABLE_ID)
_create_annot_files(jsons_content, AVAILABLE_ID)
print("JSON -> YOLO proveden!")

if POLYGON_ANNOTS:
    importlib.__import__("polygons2rectangles")
    print("Změněn typ anotací!")
