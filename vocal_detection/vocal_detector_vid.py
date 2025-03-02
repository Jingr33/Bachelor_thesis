from ultralytics import YOLO
import cv2 as cv
import torch    
import os
from moviepy.editor import ImageSequenceClip
import numpy as np


model_path = "vocal_detection/best.pt"
img_folder = "frames2"


def annotate_one_img(folder_path, img_name):
    image = cv.imread(os.path.join(folder_path, img_name))
    model = YOLO(model_path)
    
    results = model.predict(image)
    
    # empty canvas
    canvas_h = 35*3
    canvas_w = 335
    canvas = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8) * 255


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
            if (class_index in colors.keys()):
                color = colors[class_index]
                class_name = class_names[class_index]
                
            x1, y1, x2, y2 = box.xyxy[0]  # Souřadnice detekovaného objektu
            cv.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, 4)
            
            cv.rectangle(image, (0, 720 - (count + 1)*35), (335, 720 - count*35), color, -1)
            text = f"{class_name} {conf}"
            cv.putText(image, text, (5, 712 - count*35), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv.LINE_AA)
            
            # cv.rectangle(canvas, (0, canvas_h - (count + 1)*35), (335, canvas_h - count*35), color, -1)
            # text = f"{class_name} {conf}"
            # cv.putText(canvas, text, (5, canvas_h - 8 - count*35), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv.LINE_AA)

    cv.imwrite(os.path.join("annotated_frames", img_name), image)
    # cv.imwrite(os.path.join("annotated_frames", img_name), canvas)
    
    
def create_video():
    images = sorted([os.path.join("annotated_frames", img) for img in os.listdir("annotated_frames") if img.endswith('.jpg')])
    # canvases = sorted([os.path.join("annotated_frames", img) for img in os.listdir("annotated_frames") if img.endswith('.jpg')])

    fps = 30
    clip = ImageSequenceClip(images, fps=fps)
    clip.write_videofile('annotated_frames/annotated_vid_labels.mp4', codec='libx264')
    
# annotation    
img_names = sorted(img for img in os.listdir(img_folder) if img.endswith('.jpg'))
for img_name in img_names:
    annotate_one_img(img_folder, img_name)
# frames to video
create_video()