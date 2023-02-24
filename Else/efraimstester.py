import cv2
import numpy as np

# Open the video file for reading
cap = cv2.VideoCapture('/Users/efraimzetterqvist/Documents/IMG_4557.mov')

# Define the parameters for Lucas-Kanade optical flow
lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
                 flags=cv2.OPTFLOW_LK_GET_MIN_EIGENVALS)

# Take the first frame of the video
ret, old_frame = cap.read()

# Convert the first frame to grayscale
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

# Define the region of interest (ROI) where you want to track the optical flow
# You can modify these values depending on your use case
x, y, w, h = 300, 350,700, 500

# Create a mask to visualize the ROI
mask = np.zeros_like(old_frame)
cv2.rectangle(mask, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Display the mask and first frame side by side
cv2.imshow('ROI Mask', mask)
cv2.imshow('First Frame', old_frame)

# Define the initial points to track
p0 = cv2.goodFeaturesToTrack(old_gray, maxCorners=50, qualityLevel=0.01, minDistance=10, blockSize=7)

# Create a color map for visualizing the optical flow
color_map = np.random.randint(0, 255, (50, 3))

# Initialize the variables for tracking speed and direction
speed = []
direction = []

# Start the loop to read each frame and track the optical flow
while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the current frame to grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate the optical flow using Lucas-Kanade method
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # Select only the points that were successfully tracked
    good_new = p1[st == 1]
    good_old = p0[st == 1]

    # Draw the optical flow vectors
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel().astype(int)
        c, d = old.ravel().astype(int)
        mask = cv2.line(mask, (a, b), (c, d), color_map[i].tolist(), 1)
        frame = cv2.circle(frame, (a, b), 3, color_map[i].tolist(), -1)
        
        a, b = new.ravel().astype(float)
        c, d = old.ravel().astype(float)

        # Compute the magnitude and angle of the optical flow vectors
        magnitude, angle = cv2.cartToPolar(np.array([a]) - np.array([c]), np.array([b]) - np.array([d]))
        

        # Convert the angle to degrees
        angle = np.rad2deg(angle)

        # Compute the speed and direction of the optical flow vectors
        speed.append(magnitude)
        direction.append(angle)

    # Show the optical flow vectors on the current frame
    img = cv2.add(frame, mask)
    cv2.imshow('Optical Flow Vectors', img)

    # Update the variables for the next iteration
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)

    # Exit the loop if the user presses the '
    if cv2.waitKey(1) == ord('q'):
        break

# Release video capture and close all windows
cap.release()
cv2.destroyAllWindows()
print(speed)
#print(direction)
