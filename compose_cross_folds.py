"""This script split dataset into specified number of folds for cross validation.
"""

import os
import shutil

## CONFIGURATION ##
SOURCE_DATASET = "C:/bakalarka/future_dataset" # a location source folder
DESTINATION_FOLDER = "C:/bakalarka/dataset_cross" # destination folder of a new dataset
FOLDS_NUMBER = 10
CROSS_FOLDS = {
    0 : ["vid19"],
    1 : ["vid20"],
    2 : ["vid27"],
    3 : ["vid39", "vid17"],
    4 : ["vid21", "vid24"],
    5 : ["vid26", "vid36", "vid31"],
    6 : ["vid35", "vid34", "vid33", "vid25"],
    7 : ["vid32", "vid41"],
    8 : ["vid23"],
}

# CROSS_FOLDS = {
#     0 : ["vid19"],
# } # test


TEST_FOLDS = ["vid28", "vid29", "vid30"] # number of images for testing
# TEST_FOLD = ["vid17"] # test

SUBDIRS = ["images", "labels"]


def _mkdir_dataset_tree ():
    """Make a database directory tree."""
    os.makedirs(DESTINATION_FOLDER, exist_ok=True)
    for cross_fold in CROSS_FOLDS:
        for subdir in SUBDIRS:
            target_path = os.path.join(DESTINATION_FOLDER, f"fold{cross_fold}", subdir)
            os.makedirs(target_path, exist_ok = True)

    for subdir in SUBDIRS:
        test_path = os.path.join(DESTINATION_FOLDER, "test", subdir)
        os.makedirs(test_path, exist_ok=True)
    print("Strom vytvořen!")

def _create_dataset() -> None:
    file_id = 0
    for cross_key, cross_fold in CROSS_FOLDS.items():
        for folder in cross_fold:
            source_path = os.path.join(SOURCE_DATASET, folder)
            target_path = os.path.join(DESTINATION_FOLDER, f"fold{cross_key}")
            file_id = _move_folder_content(source_path, target_path, file_id)
    
    for test_folder in TEST_FOLDS:
        source_path = os.path.join(SOURCE_DATASET, test_folder)
        target_path = os.path.join(DESTINATION_FOLDER, "test")
        file_id = _move_folder_content(source_path, target_path, file_id)


def _move_folder_content(source_path, target_path, next_file_id : int) -> None:
    enum_folder = list(os.listdir(os.path.join(source_path, SUBDIRS[0])))
    count = 0
    for source_img_name in enum_folder:
        source_img_file = os.path.join(source_path, SUBDIRS[0], source_img_name)
        source_annot_name = f"{os.path.splitext(source_img_name)[0]}.txt"
        source_annot_file = os.path.join(source_path, SUBDIRS[1], source_annot_name)

        if os.path.isfile(source_img_file):
            prefix = next_file_id + count
            img_suffix = os.path.splitext(source_img_name)[1]
            target_img_name = f"{prefix}{img_suffix}"
            img_target = os.path.join(target_path, SUBDIRS[0], target_img_name)
            shutil.copy2(source_img_file, img_target)

        if os.path.isfile(source_annot_file):
            prefix = next_file_id + count
            target_annot_name = f"{prefix}.txt"
            annot_target = os.path.join(target_path, SUBDIRS[1], target_annot_name)
            shutil.copy2(source_annot_file, annot_target)

        count += 1
        
    print(f"Obsah složky {source_path} přesunut do {target_path}.")
    next_file_id += len(enum_folder) + 1
    return next_file_id

def _create_dataset_content_file() -> None:    
    file_content = "OBSAH DATASETU:\n\n"
    
    for cross_num, cross_folds in CROSS_FOLDS.items():
        for cross_fold in cross_folds:
            file_content += f"FOLD{cross_num}: {cross_fold}\n"
        file_content += "\n"

    for test_fold in TEST_FOLDS:      
        file_content += f"TEST FOLD: {test_fold}\n"
    
    with open(os.path.join(DESTINATION_FOLDER, "co_je_v_datasetu.txt"), 'w', encoding='utf-8') as f:
        f.write(file_content)

_mkdir_dataset_tree()
_create_dataset()
_create_dataset_content_file()
print("Dataset vytvořen!")
