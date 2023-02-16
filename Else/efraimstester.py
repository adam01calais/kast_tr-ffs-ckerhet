import cv2

# Open the video file
video = cv2.VideoCapture("/Users/efraimzetterqvist/Documents/IMG_1159.mov")

# Get the frame rate of the video
frame_rate = video.get(cv2.CAP_PROP_FPS)
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Print the frame rate
print("Frame rate: ", frame_rate, "Frame width: ", frame_width, "Frame_height: ", frame_height)

# Release the video
video.release()
