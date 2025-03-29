""" This code converts annotated images in jsons (COCO) to YOLO dataset format.
"""

import os
import sys
import json
import base64
from io import BytesIO
sys.path.append(r"C:\\Users\\ingrj\\AppData\\Roaming\\Python\\Python312\\site-packages")
from PIL import Image


PATH = "C:/bakalarka/test" # a location of the json file
JSON_FILE = "result.json" # a json annotated images
VAL_COUNT = 0 # number of images for validation
TEST_COUNT = 0 # number of images for testing

DIR = "dataset"
SUBDIRS = ["valid", "test", "train"]

def _mkdir_dataset(dir_path, subdirs):
    """Make a database directory tree."""
    for subdir in subdirs:
        for subsubdir in ["images", "labels"]:
            sub_sub_path = os.path.join(dir_path, subdir, subsubdir)
            if not os.path.isdir(sub_sub_path):
                os.makedirs(sub_sub_path, exist_ok = True)

def _save_images(contents, dir_path, first_id : int) -> None:
    """Save an image into the images folder."""
    for image in contents["images"]:
        image_data = base64.b64decode(image["file_name"].replace("data:image/jpg;base64,", ""))
        subdir = _get_final_folder(image["id"])
        image_name = f"{int(image["id"]) + first_id}.jpg"
        image = Image.open(BytesIO(image_data))
        image.save(os.path.join(dir_path, subdir, "images", image_name))

def _create_annotations(contents, dir_path, first_id : int) -> None:
    """Save an annotation into the labels folder in yolo format."""
    for annot in contents["annotations"]:
        # annotation.txt name
        subdir = _get_final_folder(annot["image_id"])
        annot_name = f"{int(annot["image_id"]) + first_id}.txt"
        annot_path = os.path.join(dir_path, subdir, "labels", annot_name)
        ## annotation file content
        annot_category = str(annot["category_id"])
        coords_list = _normalize_coords(contents, annot)
        annot_coords = str(coords_list).replace(",", "").replace("[", "").replace("]", "")
        file_line = f"{annot_category} {annot_coords}\n"

        with open (annot_path, "a", encoding='utf-8') as f:
            f.write(file_line)

def _normalize_coords (contents, annot) -> list:
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

def _get_final_folder (item_id : int) -> str:
    """Return the correct subdir (train/test/valid) for savig images and annotations."""
    if item_id >= VAL_COUNT + TEST_COUNT:
        return SUBDIRS[2]
    if item_id >= VAL_COUNT:
        return SUBDIRS[1]
    return SUBDIRS[0]

def _create_config_file (contents):
    """Create a configuration file for a YOLO model."""
    cat_names = list(map(lambda d: d.get("name", ""), contents["categories"]))
    text = [
        f"path: {PATH}\n",
        f"train: {os.path.join(DIR, SUBDIRS[2], "images")}\n",
        "\n",
        f"nc: {len(contents["categories"])}\n",
        f"names: {cat_names}\n",
    ]

    if TEST_COUNT > 0:
        text.insert(2, f"test: {os.path.join(DIR, SUBDIRS[1], "images")}\n")
    if VAL_COUNT > 0:
        text.insert(2, f"val: {os.path.join(DIR, SUBDIRS[0], "images")}\n")

    with open (os.path.join(PATH, "config.yaml"), "w", encoding='utf-8') as c:
        c.writelines(text)

def _next_file_id () -> int:
    """Find a first free id for a txt and jpg file names in the dataset."""
    directories = [os.path.join(PATH, DIR, SUBDIRS[0], "images"),
                   os.path.join(PATH, DIR, SUBDIRS[1], "images"),
                   os.path.join(PATH, DIR, SUBDIRS[2], "images")]
    highest_num = 0

    for directory in directories:
        for file_name in os.listdir(directory):
            num = file_name.split(".")[0]
            if num.isdigit():
                highest_num = max(highest_num, int(num))
    return int(highest_num) + 1

with open(os.path.join(PATH, JSON_FILE), 'r', encoding='UTF-8') as j:
    json_contents = json.loads(j.read())

DATASET_PATH = os.path.join(PATH, DIR)
_mkdir_dataset(DATASET_PATH, SUBDIRS)
AVAILABLE_ID = _next_file_id()
_save_images(json_contents, DATASET_PATH, AVAILABLE_ID)
_create_annotations(json_contents, DATASET_PATH, AVAILABLE_ID)
_create_config_file(json_contents)
