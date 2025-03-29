""" This script anotate frames and create annotated video.
"""

import os
import sys
sys.path.append(r"C:\\Users\\ingrj\\AppData\\Roaming\\Python\\Python312\\site-packages")
import cv2 as cv
import numpy as np
from ultralytics import YOLO
from moviepy.editor import ImageSequenceClip


SOURCE_FOLDER = "frames"
MODEL_FOLDER = "vocal_detection/nano93.pt"


def annotate_one_img(folder_path, img_name) -> None:
    """ Annotate one image, draw annotations into image and save it."""
    image = cv.imread(os.path.join(folder_path, img_name))
    model = YOLO(MODEL_FOLDER)
    results = model.predict(image)

    colors = {
        2 : (40, 39, 214),
        4 : (180, 119, 31),
        0 : (120, 187, 255),
        "default" : (0, 255, 0),
    }
    class_names = {
        2 : "left vocal fold",
        4 : "right vocal fold",
        0 : "glottic slit",
        "default" : "unknown",
    }

    for result in results:
        for box in result.boxes:
            class_index = int(box.cls.item())
            count = int(class_index / 2)
            conf = np.round(box.conf.item(), 2)
            color = colors["default"]
            class_name = class_names["default"]
            if class_index in colors.keys():
                color = colors[class_index]
                class_name = class_names[class_index]

            x1, y1, x2, y2 = box.xyxy[0]  # Souřadnice detekovaného objektu
            cv.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, 4)

            cv.rectangle(image, (0, 720 - (count + 1)*35), (335, 720 - count*35), color, -1)
            text = f"{class_name} {conf}"
            cv.putText(image, text, (5, 712 - count*35),
                       cv.FONT_HERSHEY_SIMPLEX,
                       1,
                       (0, 0, 0),
                       2,
                       cv.LINE_AA)

    cv.imwrite(os.path.join("annotated_frames", img_name), image)

def create_video():
    """ Compose video from frames. """
    max_id = len(os.listdir("annotated_frames"))
    images = []
    for i in range(1, max_id + 1):
        images.append(f"annotated_frames/{i}.jpg")
    
    fps = 24
    clip = ImageSequenceClip(images, fps=fps)
    clip.write_videofile('annotated_frames/annotated_video.mp4', codec='libx264')

os.makedirs("annotated_frames", exist_ok=True)
# img_names = sorted(img for img in os.listdir(SOURCE_FOLDER) if img.endswith('.jpg'))
# for name in img_names:
#     annotate_one_img(SOURCE_FOLDER, name)
create_video()
