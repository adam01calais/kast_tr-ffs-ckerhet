import cv2

# Open the video file
video = cv2.VideoCapture("/Users/efraimzetterqvist/Documents/IMG_1159.mov")

# Get the frame rate of the video
fps = video.get(cv2.CAP_PROP_FPS)

# Print the frame rate
print("Frame rate: ", fps)

# Release the video
video.release()
