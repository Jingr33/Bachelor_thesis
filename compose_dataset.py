"""This code compose YOLO dataset tree and add data to each section (train, validation, test).
"""

import os
import shutil

## CONFIGURATION ##
SOURCE_FOLDER = "C:/bakalarka/future_dataset" # a location source folder
DESTINATION_FOLDER = "C:/bakalarka/" # destination folder of a new dataset
VAL_FOLDERS = ["vid30", "vid20", "vid33"] # number of images for validation
TEST_FOLDERS = ["vid34", "vid19", "vid26"] # number of images for testing

DATASET_DIR = "dataset2"
SECTION_DIRS = ["valid", "test", "train"]
SECTION_SUBDIRS = ["images", "labels"]


def _mkdir_dataset_tree ():
    """Make a database directory tree."""
    for section_dir in SECTION_DIRS:
        for subdir in SECTION_SUBDIRS:
            target_path = os.path.join(DESTINATION_FOLDER, DATASET_DIR, section_dir, subdir)
            if (not os.path.isdir(target_path)):
                os.makedirs(target_path, exist_ok = True)
    print("Strom vytvořen!")

def _create_dataset() -> None:
    file_id = 0
    for folder in os.listdir(SOURCE_FOLDER):
        source_path = os.path.join(SOURCE_FOLDER, folder)
        target_path = _choose_target_folder(folder)
        file_id = _move_folder_content(source_path, target_path, file_id)

def _choose_target_folder(folder) -> str:
    folder_dir = "train"
    if folder in VAL_FOLDERS:
        folder_dir = "valid"
    elif folder in TEST_FOLDERS:
        folder_dir = "test"
    return os.path.join(DESTINATION_FOLDER, DATASET_DIR, folder_dir)
      
def _move_folder_content(source_path, target_path, next_file_id : int) -> None:
    enum_folder = list(os.listdir(os.path.join(source_path, SECTION_SUBDIRS[0])))
    count = 0
    for source_img_name in enum_folder:
        source_img_file = os.path.join(source_path, SECTION_SUBDIRS[0], source_img_name)
        source_annot_name = f"{os.path.splitext(source_img_name)[0]}.txt"
        source_annot_file = os.path.join(source_path, SECTION_SUBDIRS[1], source_annot_name)

        if os.path.isfile(source_img_file) and os.path.isfile(source_annot_file):
            prefix = next_file_id + count
            img_suffix = os.path.splitext(source_img_name)[1]
            target_img_name = f"{prefix}{img_suffix}"
            target_annot_name = f"{prefix}.txt"

            img_target = os.path.join(target_path, SECTION_SUBDIRS[0], target_img_name)
            annot_target = os.path.join(target_path, SECTION_SUBDIRS[1], target_annot_name)
            shutil.copy2(source_img_file, img_target)
            shutil.copy2(source_annot_file, annot_target)
        count += 1

    next_file_id += len(enum_folder) + 1
    print(f"Přidány soubory ze složky: {source_path}")
    return next_file_id

    
_mkdir_dataset_tree()
_create_dataset()
print("HOTOVO!!!")