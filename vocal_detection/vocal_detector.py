""" Draw annotation into png image.
"""

import cv2 as cv
import numpy as np
from ultralytics import YOLO


MODEL = YOLO("vocal_detection/best.pt")
IMG_FOLDER = "vocal_detection/hlasivka"

image = cv.imread(IMG_FOLDER + ".png")
results = MODEL.predict(image)

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
    COUNT = 0
    for box in result.boxes:
        class_index = int(box.cls.item())
        conf = np.round(box.conf.item(), 2)
        color = colors["default"]
        CLASS_NAME = class_names["default"]
        if (class_index in colors.keys() and conf > 0.6):
            color = colors[class_index]
            CLASS_NAME = class_names[class_index]
            x1, y1, x2, y2 = box.xyxy[0]  # Souřadnice detekovaného objektu
            cv.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, 3)

            cv.rectangle(image, (600, 670 + (COUNT + 1)*35), (1035, 670 + COUNT*35), color, -1)
            TEXT = f"{CLASS_NAME} {conf}"
            cv.putText(image, TEXT, (605, 662 + (COUNT + 1)*35),
                       cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv.LINE_AA)
            COUNT += 1

cv.imwrite(IMG_FOLDER + "_prediction.png", image)
cv.imshow("predikce", image)
cv.waitKey(0)
cv.destroyAllWindows()
