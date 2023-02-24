import cv2

# Load the video and create a VideoCapture object
cap = cv2.VideoCapture('/Users/efraimzetterqvist/Documents/IMG_1161.mov')

# Extract the first frame as the background image
_, bg = cap.read()
bg_gray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)

# Define the threshold for detecting the ball
threshold = 100

# Define the minimum area for the ball
min_area = 500

# Loop through the video frames
while True:
    # Read the current frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the current frame to grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Subtract the background from the current frame
    diff = cv2.absdiff(bg_gray, frame_gray)

    # Apply a threshold to the difference image
    _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

    # Apply morphological operations to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    thresh = cv2.erode(thresh, kernel, iterations=2)
    thresh = cv2.dilate(thresh, kernel, iterations=2)

    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through the contours
    for contour in contours:
        # Calculate the area of the contour
        area = cv2.contourArea(contour)

        # If the area is larger than the minimum area, it is likely a ball
        if area > min_area:
            # Draw a bounding box around the ball
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Display the current frame
    cv2.imshow('frame', frame)

    # Check for key press
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()
