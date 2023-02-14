# import cv2
# import numpy as np

# videoCapture=cv2.VideoCapture('/Users/efraimzetterqvist/Library/Mobile Documents/com~apple~CloudDocs/Chalmers/IMG_1160.mov')
# prevCircle = None
# dist = lambda x1, y1, x2, y2: (x1-x2)**2+(y1-y2)**2

# while True:
#     ret, frame = videoCapture.read()
#     if not ret: break

#     grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     blurFrame = cv2.GaussianBlur(grayFrame, (23,23), 0)

#     circles = cv2.HoughCircles(blurFrame, cv2.HOUGH_GRADIENT, 1.2, 100, param1=100, param2=30, minRadius=25, maxRadius=300)

#     if circles is not None:
#         circles = np.uint16(np.around(circles))
#         chosen = None
#         for i in circles[0, :]:
#             if chosen is None: chosen = i
#             if prevCircle is not None:
#                 if dist(chosen[0],chosen[1],prevCircle[0],prevCircle[1]) <= dist(i[0],i[1],prevCircle[0],prevCircle[1]):
#                     chosen=i
#         cv2.circle(frame, (chosen[0], chosen[1]), 1, (0,100,100), 3)
#         cv2.circle(frame, (chosen[0], chosen[1]), chosen[2], (255,0,255),3)
#         prevCircle=chosen

#     cv2.imshow('Circles', frame)


#     if cv2.waitKey(1) & 0xFF == ord('q'): break

# videoCapture.release()
# cv2.destroyAllWindows()
base64 images-8.jpeg | curl -d @- \
"https://detect.roboflow.com/dodgeball-detection/1?api_key=CPkBglSIfMhKhrghnYcq"