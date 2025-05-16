""" This script compose a partial dataset for cross validation training.  
"""

import os
import shutil

## CONFIGURATION ##
SOURCE_FOLDER = "C:/bakalarka/dataset_cross" # a location source folder
DESTINATION_FOLDER = "C:/bakalarka/partial_dataset10" # destination folder of a new dataset
VALIDATION_FOLD = "fold9" # specify fold for with validation data

SUBDIRS = ["train", "valid", "test"]
SUBSUBDIRS = ["images", "labels"]


def _mkdir_dataset_tree ():
    """Make a database directory tree."""
    for subdir in SUBDIRS:
        for subsubdir in SUBSUBDIRS:
            target_path = os.path.join(DESTINATION_FOLDER, subdir, subsubdir)
            os.makedirs(target_path, exist_ok = True)
    print("Adresářový strom vytvořen!")

def _create_dataset() -> None:
    file_id = 0
    source_test = os.path.join(SOURCE_FOLDER, "test")
    target_test = os.path.join(DESTINATION_FOLDER, SUBDIRS[2])
    file_id = _move_folder_content(source_test, target_test, file_id)
    
    source_val = os.path.join(SOURCE_FOLDER, VALIDATION_FOLD)
    target_val = os.path.join(DESTINATION_FOLDER, SUBDIRS[1])
    file_id = _move_folder_content(source_val, target_val, file_id)
    
    TRAIN_FOLDS = [fold for fold in os.listdir(SOURCE_FOLDER) 
                   if os.path.isdir(os.path.join(SOURCE_FOLDER, fold)) 
                   and fold != "test" and fold != VALIDATION_FOLD]
    for train_fold in TRAIN_FOLDS:
        source_train = os.path.join(SOURCE_FOLDER, train_fold)
        target_train = os.path.join(DESTINATION_FOLDER, SUBDIRS[0])
        file_id = _move_folder_content(source_train, target_train, file_id)

def _move_folder_content(source_path, target_path, next_file_id : int) -> None:
    enum_folder = list(os.listdir(os.path.join(source_path, SUBSUBDIRS[0])))
    count = 0
    for source_img_name in enum_folder:
        source_img_file = os.path.join(source_path, SUBSUBDIRS[0], source_img_name)
        source_annot_name = f"{os.path.splitext(source_img_name)[0]}.txt"
        source_annot_file = os.path.join(source_path, SUBSUBDIRS[1], source_annot_name)

        if os.path.isfile(source_img_file):
            prefix = next_file_id + count
            img_suffix = os.path.splitext(source_img_name)[1]
            target_img_name = f"{prefix}{img_suffix}"
            img_target = os.path.join(target_path, SUBSUBDIRS[0], target_img_name)
            shutil.copy2(source_img_file, img_target)

        if os.path.isfile(source_annot_file):
            prefix = next_file_id + count
            target_annot_name = f"{prefix}.txt"
            annot_target = os.path.join(target_path, SUBSUBDIRS[1], target_annot_name)
            shutil.copy2(source_annot_file, annot_target)

        count += 1

    next_file_id += len(enum_folder) + 1
    print(f"Obsah složky {source_path} přesunut do {target_path}")
    return next_file_id

def _create_dataset_content_file() -> None:
    source_data = {
        SUBDIRS[0] : [],
        SUBDIRS[1] : [],
        SUBDIRS[2] : [],
    }
    with open(os.path.join(SOURCE_FOLDER, "co_je_v_datasetu.txt"), "r", encoding='utf-8') as f:
        for line in f.readlines():
            if "TEST FOLD" in line:
                source_data[SUBDIRS[2]].append(line.lstrip("TEST FOLD: "))
            elif VALIDATION_FOLD in line:
                source_data[SUBDIRS[1]].append(line.split(" ")[1])
            elif "FOLD" in line:
                source_data[SUBDIRS[0]].append(line.split(" ")[1])

    file_content = f"OBSAH PARCIÁLNÍHO DATASETU\n\n"
    test_data_str = str(source_data[SUBDIRS[2]]).replace('[', '').replace(']', '').replace("'", "").replace(', ', '').replace('\\n', '\n')
    file_content += f"TESTOVACÍ DATA:\n{test_data_str}\n\n"    
    val_data_str = str(source_data[SUBDIRS[1]]).replace('[', '').replace(']', '').replace("'", "").replace(', ', '').replace('\\n', '\n')
    file_content += f"VALIDAČNÍ DATA:\n{val_data_str}\n\n"    
    train_data_str = str(source_data[SUBDIRS[0]]).replace('[', '').replace(']', '').replace("'", "").replace(', ', '').replace('\\n', '\n')
    file_content += f"TRÉNOVACÍ DATA:\n{train_data_str}\n"    
        
    with open(os.path.join(DESTINATION_FOLDER, "co_je_v_datasetu.txt"), 'w', encoding='utf-8') as f:
        f.write(file_content)

_mkdir_dataset_tree()
_create_dataset()
_create_dataset_content_file()
print("Dataset vytvořen!")
