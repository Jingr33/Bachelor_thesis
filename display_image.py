import json
import base64
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt


with open("result.json", 'r') as j:
    contents = json.loads(j.read())

print(contents.keys())
print(len(contents["images"]))
for image in contents["images"]:
    print(image["file_name"])
    image_data = base64.b64decode(image["file_name"].replace("data:image/jpg;base64,", ""))
    image = Image.open(BytesIO(image_data))

    # Plot the image using matplotlib
    plt.imshow(image)
    plt.axis('off')  # Hide axis
    plt.show()