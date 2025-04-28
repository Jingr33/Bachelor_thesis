""" This script displayes images with its POLYGONAL annotations from folder in YOLO format. 
""" 

import sys
import os
sys.path.append(r"C:\\Users\\ingrj\\AppData\\Roaming\\Python\\Python312\\site-packages")
import cv2
import numpy


DATASET_PATH = "future_dataset/vid27_corr"

def _resize_image(raw_image) -> int:
    orig_h, orig_w, _ = raw_image.shape
    new_w = 1000
    new_h = int(orig_h * new_w / orig_w)
    return cv2.resize(raw_image, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

for file_name in os.listdir(os.path.join(DATASET_PATH, "images")):
    image_raw = cv2.imread(os.path.join(DATASET_PATH, "images", file_name))
    image = _resize_image(image_raw)
    height, width, channels = image.shape

    labels = []
    annot_path = os.path.join(DATASET_PATH, "labels", file_name.split(".")[0] + ".txt")
    if os.path.exists(annot_path):
        with open (annot_path, "r", encoding='utf-8') as f:
            labels = f.readlines()

        annotations = [None] * len(labels)
        start_points = []
        end_points = []
        annot_class = []
        for label, i in enumerate(labels):
            annot_list = label.replace("\n", "").split(" ")
            annot_class.append(int(annot_list[0]))
            del annot_list[0]
            points_length = int(len(annot_list) / 2)
            points = [None] * points_length
            for j in range(points_length):
                points[j] = (float(annot_list[j * 2]) * width,
                             float(annot_list[j * 2 + 1]) * height)
            annotations[i] = points

        THICKNESS = 2
        COLOR = (0, 255, 0)
        class_colors = {
            -1 : COLOR,
            2 : (40, 39, 214),
            4 : (180, 119, 31),
            0 : (120, 187, 255),
        }

        for annotation, k in (annotations):
            cv2.polylines(image,
                          numpy.array([annotation], dtype=numpy.int32),
                          isClosed=True,
                          color = class_colors[annot_class[k]],
                          thickness = THICKNESS)

    cv2.imshow(file_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
