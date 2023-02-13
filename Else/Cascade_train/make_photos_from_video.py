import cv2
import os

# Define the video path
video_path = "/Users/efraimzetterqvist/Library/Mobile Documents/com~apple~CloudDocs/Chalmers/IMG_1139.MOV"

# Define the folder to save the frames
frames_folder = "/Users/efraimzetterqvist/Documents/GitHub/kast_tr-ffs-ckerhet/Else/Cascade_train/positive"

# Open the video using OpenCV
cap = cv2.VideoCapture(video_path)

# Check if the video was opened successfully
if not cap.isOpened():
    print("Error opening video")

# Get the number of frames in the video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Loop through each frame of the video
for i in range(total_frames):
    # Read the frame
    ret, frame = cap.read()

    # Check if the frame was read successfully
    if ret:
        # Save the frame as an image
        filename = os.path.join(frames_folder, "frame_{}.png".format(i))
        cv2.imwrite(filename, frame)
    else:
        # Break the loop if the frame was not read successfully
        break

# Release the video capture
cap.release()
