""" Script for override polygons annotations to rectagle variant.
"""

import os
import sys
sys.path.append(r"C:\\Users\\ingrj\\AppData\\Roaming\\Python\\Python312\\site-packages")
import numpy as np


# folder with polygon annotations in txt files
PATH = "future_dataset/vid20_corr/bels"


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

for file in os.listdir(PATH):
    file_path = os.path.join(PATH, file)
    POLY_ANNOTS = ""
    with open(file_path, "r", encoding="utf-8") as file:
        POLY_ANNOTS = file.readlines()

    RECT_ANNOTS = ""
    for annot in POLY_ANNOTS:
        RECT_ANNOTS += _polygon2rectangle(annot)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(RECT_ANNOTS)
