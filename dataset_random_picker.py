import json
import base64
from io import BytesIO
from PIL import Image
import os
import numpy as np
import random
from pathlib import Path


num_of_imgs = 30
transfer_to = "valid"

dir = "C:/python/dataset_only_train/"

def _transfer_files (suffixes : list, names : list) -> None:
    for index in indexes:
        for suffix in suffixes:
            file_name = f"{index}.{suffix}"
            final_folder = _get_final_folder(suffix)
            original_path = os.path.join(dir, "train", final_folder, file_name)
            new_path = os.path.join(dir, transfer_to, final_folder, file_name)
            if os.path.isfile(original_path):
                os.replace(original_path, new_path)

def _get_final_folder (suffix : str):
    if (suffix == "jpg"):
        return "images"
    elif (suffix == "txt"):
        return "labels"
    return None

def _get_ds_size ():
    highest_num = 0
    for file_name in os.listdir(os.path.join(dir, "train/images")):
        num = file_name.split(".")[0]
        if num.isdigit() and int(num) > int(highest_num):
            highest_num = num
    return int(highest_num)

def _get_rnd_indexes (ds_size):
    indexes = []
    if ds_size < len(indexes): return
    while len(indexes) != num_of_imgs:
        index = random.randint(1, ds_size)
        if not index in indexes:
            indexes.append(index)
    return indexes

ds_size = _get_ds_size()
indexes = _get_rnd_indexes(ds_size)
suffixes = ["jpg", "txt"]
_transfer_files(suffixes, indexes)
