# import cv2

# # Load the video file
# video = cv2.VideoCapture("/Users/efraimzetterqvist/Library/Mobile Documents/com~apple~CloudDocs/Documents/IMG_2768.mov")

# # Check if the video was successfully opened
# if not video.isOpened():
#     print("Error: Could not open the video file.")
#     exit()

# # Loop over each frame of the video
# while True:
#     # Read the next frame from the video
#     ret, frame = video.read()

#     # Break out of the loop if we have reached the end of the video
#     if not ret:
#         break

#     # Display the current frame
#     cv2.imshow("Video", frame)

#     # Break out of the loop if the user presses the 'q' key
#     if cv2.waitKey(25) & 0xFF == ord('q'):
#         break

# # Release the video file and close all windows
# video.release()
# cv2.destroyAllWindows()

import cv2

<<<<<<< HEAD
# Load the image file
img = cv2.imread("image.jpg")
=======
# Load the video file
video = cv2.VideoCapture("\Users\Joakim\Documents\3an\Kandidatarbete")
>>>>>>> bc93c1459acd369854baef830182c81b1cb24c70

# Check if the image was successfully loaded
if img is None:
    print("Error: Could not load the image file.")
    exit()

# Display the image
cv2.imshow("Image", img)

# Wait for the user to close the window
cv2.waitKey(0)

# Close all windows
cv2.destroyAllWindows()
