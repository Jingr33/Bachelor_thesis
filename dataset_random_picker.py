""" This script choose specified number of items from YOLO dataset and transfer it
    into target folder.
"""

import os
import random


DATASET_PATH = "C:/python/dataset/"
TARGET_FOLDER = "valid"
IMAGES_NUM = 30


def _transfer_files (indexes : list) -> None:
    """Transfer files containing specified indexes to target folder."""
    for index in indexes:
        for suffix in ["jpg", "txt"]:
            file_name = f"{index}.{suffix}"
            final_folder = _get_final_folder(suffix)
            orig_path = os.path.join(DATASET_PATH, "train", final_folder, file_name)
            new_path = os.path.join(DATASET_PATH, TARGET_FOLDER, final_folder, file_name)
            if os.path.isfile(orig_path):
                os.replace(orig_path, new_path)

def _get_final_folder(suffix : str) -> str:
    """Return 'images' folder for image or 'labels' folder for annotation file."""
    if suffix == "jpg":
        return "images"
    if suffix == "txt":
        return "labels"
    return None

def _get_ds_size() -> int:
    """ Return size of dataset."""
    highest_num = 0
    for img_name in os.listdir(os.path.join(DATASET_PATH, "train/images")):
        idx = img_name.split(".")[0]
        if idx.isdigit() and int(idx) > highest_num:
            highest_num = int(idx)
    return highest_num

def _get_rnd_indexes(ds_size : int) -> list:
    indexes = []
    if ds_size < len(indexes):
        return None
    while len(indexes) != IMAGES_NUM:
        index = random.randint(1, ds_size)
        if not index in indexes:
            indexes.append(index)
    return indexes

DATASET_SIZE = _get_ds_size()
idx_list = _get_rnd_indexes(DATASET_SIZE)
_transfer_files(idx_list)
