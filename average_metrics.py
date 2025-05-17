import sys
sys.path.append(r"C:\\Users\\ingrj\\AppData\\Roaming\\Python\\Python312\\site-packages")
import numpy as np

metrics = [0.719, 0.599, 0.423, 0.443, 0.589, 0.625, 0.550, 0.612, 0.736]

print(np.average(metrics))