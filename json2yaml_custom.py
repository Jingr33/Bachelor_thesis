"""This code converts json file with images and its annotations in YOLO format of annotations with image and annotation txt file 
"""

import json
import base64
from io import BytesIO
from PIL import Image
import os
import numpy as np

## CONFIGURATION ##
JSON_FILE = "C:/bakalarka/jsons/vid31c.json" # a source json file name
TARGET_DIR = "C:/bakalarka/future_dataset/vid31" # target path to directory with YOLO dataset
POLYGON_ANNOTS = True # treu if annotation type of images is polygonal, false if rectangular


PACIENT_SUBDIRS = ["images", "labels"]

def _mkdir_dataset () -> int:
    """Prepare tree structure of folders for YOLO dataset of one pacient.
    
    Return:
        int: next avalaible index in dataset folder, if new folder is created, return next_id = 0
    """
    for subdir in PACIENT_SUBDIRS:
        path = os.path.join(TARGET_DIR, subdir)
        if (not os.path.isdir(path)):
            os.makedirs(path, exist_ok = True)
                        
def _next_file_id () -> int:
    """Find a first available id for a txt and jpg file names in the dataset."""
    highest_num = 0
    DIR = os.path.join(TARGET_DIR, PACIENT_SUBDIRS[0])
    for file_name in os.listdir(DIR):
        num = file_name.split(".")[0]
        if num.isdigit():
            num = int(num)
            if num > highest_num:
                highest_num = num
    return int(highest_num) + 1

def _save_images (contents, first_id : int) -> None:
    """Save an image into the images folder."""
    for image in contents["images"]:
        image_data = base64.b64decode(image["file_name"].replace("data:image/jpg;base64,", ""))
        image_name = f"{image["id"] + first_id}.jpg"
        image = Image.open(BytesIO(image_data))
        image.save(os.path.join(TARGET_DIR, PACIENT_SUBDIRS[0], image_name))
    
def _create_annot_files (contents, first_id : int) -> None:
    """Save an annotation into the labels folder in yolo format."""
    for annot in contents["annotations"]:
        # create annotation.txt file name
        annot_name = f"{annot["image_id"] + first_id}.txt"
        annot_path = os.path.join(TARGET_DIR, PACIENT_SUBDIRS[1], annot_name)
        ## annotation file content
        annot_category = str(annot["category_id"])
        coords_list = _normalize_coords(contents, annot)
        annot_coords = str(coords_list).replace(",", "").replace("[", "").replace("]", "")
        file_line = "{0} {1}\n".format(annot_category, annot_coords)
        # save
        with open (annot_path, "a") as f:
            f.write(file_line)
            
def _normalize_coords (contents, annot) -> list:
    """method for normalizing annotation coordinates."""
    image = next((item for item in contents["images"] if item["id"] == annot["image_id"]), None)
    width = image["width"]
    height = image["height"]
    for i in range(len(annot["segmentation"][0])):
        if (i % 2 == 0):
            annot["segmentation"][0][i] = annot["segmentation"][0][i] / width
        else:
            annot["segmentation"][0][i] = annot["segmentation"][0][i] / height
    return annot["segmentation"]
        

# def _get_final_folder (id) -> str:
#     """Return the correct subdir for savig images and annotations."""
#     if (id >= VAL_NUM + TESTNUM):
#         return SUBDIRS[2]
#     elif (id >= VAL_NUM):
#         return SUBDIRS[1]
#     return SUBDIRS[0]

# def _create_config_file (contents):
#     """Create a configuration file for a yolo model."""
#     cat_names = list(map(lambda d: d.get("name", ""), contents["categories"]))
#     text = [
#         "path: {0}\n".format(PATH),
#         "train: {0}\n".format(os.path.join(DIR, SUBDIRS[2], "images")),
#         "\n",
#         "nc: {0}\n".format(len(contents["categories"])),
#         "names: {0}\n".format(cat_names),
#     ]
    
#     if (TESTNUM > 0):
#         text.insert(2, "test: {0}\n".format(os.path.join(DIR, SUBDIRS[1], "images")))
#     if (VAL_NUM > 0):
#         text.insert(2, "val: {0}\n".format(os.path.join(DIR, SUBDIRS[0], "images")))
        
#     with open (os.path.join(PATH, "config.yaml"), "w") as c:
#         c.writelines(text)
        
# def _next_file_id () -> int:
#     """Find a first free id for a txt and jpg files names in the dataset."""
#     highest_num = 0
#     directories = [os.path.join(PATH, DIR, SUBDIRS[0], "images"), os.path.join(PATH, DIR, SUBDIRS[1], "images"),os.path.join(PATH, DIR, SUBDIRS[2], "images")]
#     for directory in directories:
#         for file_name in os.listdir(directory):
#             num = file_name.split(".")[0]
#             if num.isdigit():
#                 num = int(num)
#                 if num > highest_num:
#                     highest_num = num
#     return int(highest_num) + 1

def _polygon2rectangle(annotation : str) -> str:
    poly_coords = annotation.replace("\n", "").split(" ")
    annot_class = int(poly_coords[0])
    x_coords, y_coords = [], []
    for i in range(1, len(poly_coords), 2):
        x_coords.append(float(poly_coords[i]))
        y_coords.append(float(poly_coords[i + 1]))

    x_max, x_min = max(x_coords), min(x_coords)
    y_max, y_min = max(y_coords), min(y_coords)
    x = np.average((x_max, x_min))
    y = np.average((y_max, y_min))
    w = x_max - x_min
    h = y_max - y_min
    return f"{annot_class} {x} {y} {w} {h}\n"

def _create_rectangle_annotations() -> None:
    annot_folder = os.path.join(TARGET_DIR, PACIENT_SUBDIRS[1])
    for item in os.listdir(annot_folder):
        file_path = os.path.join(annot_folder, item)
        with open(file_path, "r+", encoding="utf-8") as file:
            poly_annots = file.readlines()
            rect_annots = ""
            for annot in poly_annots:
                rect_annots += _polygon2rectangle(annot)
            file.seek(0)
            file.write(rect_annots)
            file.truncate()
           

with open(JSON_FILE, 'r') as j:
    contents = json.loads(j.read())

print(f"Vytvářím dataset ve složce {TARGET_DIR}...")    
_mkdir_dataset()
first_id = _next_file_id()
_save_images(contents, first_id)
_create_annot_files(contents, first_id)
print("JSON -> YOLO proveden!")

if (POLYGON_ANNOTS):
    _create_rectangle_annotations()
    print("Změněn typ anotací!")
