""" Script for override polygons annotations to rectagle variant.
"""

import os
import numpy as np

FOLDER = "p2r"

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

for item in os.listdir(FOLDER):
    file_path = os.path.join(FOLDER, item)
    with open(file_path, "r+", encoding="utf-8") as file:
        poly_annots = file.readlines()
        rect_annots = ""
        for annot in poly_annots:
            rect_annots += _polygon2rectangle(annot)
        file.seek(0)
        file.write(rect_annots)
        file.truncate()
