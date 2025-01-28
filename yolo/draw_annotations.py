import cv2
import numpy
import os

path = "C:/python/dataset/train"
file_name = "2000"
image = cv2.imread(os.path.join(path, "images", file_name + ".jpg"))
height, width, channels = image.shape

labels = []
with open (os.path.join(path, "labels", file_name + ".txt"), "r") as f:
    labels = f.readlines()
    
annotations = [None] * len(labels)
for i in range(len(labels)):
    annot_list = labels[i].replace("\n", "").split(" ")
    del annot_list[0]
    points_length = int(len(annot_list) / 2)
    points = [None] * points_length
    for j in range(points_length):
        points[j] = (float(annot_list[j * 2]) * width, float(annot_list[j * 2 + 1]) * height)
    annotations[i] = points
    
thickness = 3
color = (0, 255, 0)

for k in range(len(annotations)):
    cv2.polylines(image, numpy.array([annotations[k]], dtype=numpy.int32), isClosed=True, color = color, thickness = thickness)

cv2.imshow("Annotations", image)
cv2.waitKey(0)
cv2.destroyAllWindows()