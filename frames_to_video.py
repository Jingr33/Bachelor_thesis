""" This script creates mp4 video from frames. 
"""

import os
from moviepy.editor import ImageSequenceClip

FRAMES_FOLDER = "frames"
images = sorted([os.path.join(FRAMES_FOLDER, img) for img in os.listdir(FRAMES_FOLDER)
                if img.endswith('.jpg')])

FPS = 30
clip = ImageSequenceClip(images, fps=FPS)
clip.write_videofile('frames/video.mp4', codec='libx264')
