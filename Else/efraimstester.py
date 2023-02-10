import cv2

# Load the video file
video = cv2.VideoCapture("\Users\Joakim\Documents\3an\Kandidatarbete")

# Check if the video was successfully opened
if not video.isOpened():
    print("Error: Could not open the video file.")
    exit()

# Loop over each frame of the video
while True:
    # Read the next frame from the video
    ret, frame = video.read()

    # Break out of the loop if we have reached the end of the video
    if not ret:
        break

    # Display the current frame
    cv2.imshow("Video", frame)

    # Break out of the loop if the user presses the 'q' key
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Release the video file and close all windows
video.release()
cv2.destroyAllWindows()
