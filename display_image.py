""" This script display images from COCO json file. 
"""

import json
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image


with open("result.json", 'r', encoding='utf-8') as j:
    contents = json.loads(j.read())

for image in contents["images"]:
    image_data = base64.b64decode(image["file_name"].replace("data:image/jpg;base64,", ""))
    image = Image.open(BytesIO(image_data))

    print(image["file_name"])
    plt.imshow(image)
    plt.axis('off')  # Hide axis
    plt.show()
