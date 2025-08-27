import matplotlib.pyplot as plt
import numpy as np

models = ["YOLOv5s", "YOLOv5m", "YOLOv5l", "YOLOv5x"]
devices = ["Colab V100", "iPhone12 ANE", "iPhone12 GPU", "iPhone12 CPU"]
fps = [[37, 12, 12, 12],
       [31, 9, 8, 6], 
       [24, 6, 5, 3], 
       [20, 2, 3, 2]
      ]

def addlabels(y):
    for j in range(len(y)):
        for i in range(len(y[j])):
            plt.text(j + (i * 0.22) - 0.33, y[j][i] + 0.5, y[j][i], ha = 'center')

x = np.arange(len(models)) 
width = 0.2 
offset = width * 1.1

colors = ["#e94965", "#fecf16", "#4185c6", "#5dbca4"]

fig, ax = plt.subplots()
for i in range(len(devices)):
    ax.bar(x + i * offset - (1.5 * offset), [row[i] for row in fps], 
                       width, color=colors[i], label=devices[i])
    
addlabels(fps)

ax.set_xticks(x)
ax.set_xticklabels(models)

ax.set_xlabel("MODEL")
ax.set_ylabel("FPS")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1 + 0.01,
                 box.width, box.height * 0.9])

ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=False, shadow=False, ncol=5, frameon = False)

plt.show()