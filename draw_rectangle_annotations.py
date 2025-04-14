""" This script displayes images with its RECTANGLE annotations from folder in YOLO format. 
""" 

import sys
import os
sys.path.append(r"C:\\Users\\ingrj\\AppData\\Roaming\\Python\\Python312\\site-packages")
import cv2


DATASET_PATH = "future_dataset/vid19"

def _resize_image(raw_image) -> int:
    orig_h, orig_w, _ = raw_image.shape
    new_w = 1000
    new_h = int(orig_h * new_w / orig_w)
    new_image = cv2.resize(raw_image, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
    ratio = new_w / orig_w
    return new_image, ratio

COUNT = 0
for file_name in os.listdir(os.path.join(DATASET_PATH, "images")):
    COUNT +=1
    if COUNT % 11 != 0: # display only each 11th image
        continue

    image_raw = cv2.imread(os.path.join(DATASET_PATH, "images", file_name))
    image, scale = _resize_image(image_raw)
    height, width, channels = image.shape

    labels = []
    annot_path = os.path.join(DATASET_PATH, "labels", file_name.split(".")[0] + ".txt")
    if os.path.exists(annot_path):
        with open (annot_path, "r", encoding='utf-8') as f:
            labels = f.readlines()

        annotations = [None] * len(labels)
        start_points = []
        end_points = []
        obj_class = []
        for i in range(len(labels)):
            annot_list = labels[i].replace("\n", "").split(" ")
            annot_list = [float(annot_list[i]) for i in range(len(annot_list))]
            obj_class.append(int(annot_list[0]))

            x_center = annot_list[1] * width
            y_center = annot_list[2] * height
            box_width = annot_list[3] * width
            box_height = annot_list[4] * height

            start_x = int(x_center - box_width / 2)
            start_y = int(y_center - box_height / 2)
            end_x = int(x_center + box_width / 2)
            end_y = int(y_center + box_height / 2)

            start_points.append((start_x, start_y))
            end_points.append((end_x, end_y))

        THICKNESS = 1
        COLOR = (0, 255, 0)
        class_colors = {
            -1 : COLOR,
            2 : (40, 39, 214),
            4 : (180, 119, 31),
            0 : (120, 187, 255),
        }

        for i in range(len(start_points)):
            cv2.rectangle(image, start_points[i],
                          end_points[i],
                          class_colors[obj_class[i]],
                          THICKNESS)

    cv2.imshow(file_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
