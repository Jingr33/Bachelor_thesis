from moviepy.editor import ImageSequenceClip
import os

img_folder = "frames"
images = sorted([os.path.join(img_folder, img) for img in os.listdir(img_folder) if img.endswith('.jpg')])

fps = 30
clip = ImageSequenceClip(images, fps=fps)
clip.write_videofile('frames/video.mp4', codec='libx264')