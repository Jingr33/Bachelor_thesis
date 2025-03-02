"""This code converts json file with annotations to a folder tree with yaml files for yolo ai model."""

import json
import base64
from io import BytesIO
from PIL import Image
import os

## CONFIGURATION ##
json_file = "41.json" # a json file name
path = "C:/bakalarka" # a location of the json file
val_num = 0 # number of images for validation
test_num = 0 # number of images for testing

dir = "dataset"
subdirs = ["valid", "test", "train"]

def _mkdir_dataset (dir_path, subdirs):
    """Make a database directory tree."""
    for subdir in subdirs:
        for subsubdir in ["images", "labels"]:
            sub_sub_path = os.path.join(dir_path, subdir, subsubdir)
            if (not os.path.isdir(sub_sub_path)):
                os.makedirs(sub_sub_path, exist_ok = True)

def _save_images (contents, dir_path, first_id : int) -> None:
    """Save an image into the images folder."""
    for image in contents["images"]:
        image_data = base64.b64decode(image["file_name"].replace("data:image/jpg;base64,", ""))
        subdir = _get_final_folder(image["id"])
        image_name = "{0}.jpg".format(int(image["id"]) + first_id)
        image = Image.open(BytesIO(image_data))
        image.save(os.path.join(dir_path, subdir, "images", image_name))
    
def _create_annot_files (contents, dir_path, first_id : int) -> None:
    """Save an annotation into the labels folder in yolo format."""
    for annot in contents["annotations"]:
        # annotation.txt name
        subdir = _get_final_folder(annot["image_id"])
        annot_name = "{0}.txt".format(int(annot["image_id"]) + first_id)
        annot_path = os.path.join(dir_path, subdir, "labels", annot_name)
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
        

def _get_final_folder (id) -> str:
    """Return the correct subdir for savig images and annotations."""
    if (id >= val_num + test_num):
        return subdirs[2]
    elif (id >= val_num):
        return subdirs[1]
    return subdirs[0]

def _create_config_file (contents):
    """Create a configuration file for a yolo model."""
    cat_names = list(map(lambda d: d.get("name", ""), contents["categories"]))
    text = [
        "path: {0}\n".format(path),
        "train: {0}\n".format(os.path.join(dir, subdirs[2], "images")),
        "\n",
        "nc: {0}\n".format(len(contents["categories"])),
        "names: {0}\n".format(cat_names),
    ]
    
    if (test_num > 0):
        text.insert(2, "test: {0}\n".format(os.path.join(dir, subdirs[1], "images")))
    if (val_num > 0):
        text.insert(2, "val: {0}\n".format(os.path.join(dir, subdirs[0], "images")))
        
    with open (os.path.join(path, "config.yaml"), "w") as c:
        c.writelines(text)
        
def _next_file_id () -> int:
    """Find a first free id for a txt and jpg files names in the dataset."""
    highest_num = 0
    directories = [os.path.join(path, dir, subdirs[0], "images"), os.path.join(path, dir, subdirs[1], "images"),os.path.join(path, dir, subdirs[2], "images")]
    for directory in directories:
        for file_name in os.listdir(directory):
            num = file_name.split(".")[0]
            if num.isdigit():
                num = int(num)
                if num > highest_num:
                    highest_num = num
    return int(highest_num) + 1
            

with open(os.path.join(path, json_file), 'r') as j:
    contents = json.loads(j.read())
    
dir_path = os.path.join(path, dir)
_mkdir_dataset(dir_path, subdirs)
first_id = _next_file_id()
_save_images(contents, dir_path, first_id)
_create_annot_files(contents, dir_path, first_id)
_create_config_file(contents)

