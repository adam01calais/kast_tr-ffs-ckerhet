from roboflow import Roboflow
# import cv2
# import os

# video=cv2.VideoCapture("/Users/efraimzetterqvist/Library/Mobile Documents/com~apple~CloudDocs/Chalmers/IMG_1159.mov")
# i=0
# path= "/Users/efraimzetterqvist/Documents/dodge"
# while(video.isOpened()):
#     ret, frame = video.read()
#     if ret == False:
#         break
#     cv2.imwrite(os.path.join(path,'dodge'+str(i)+'.jpg'),frame)
#     i+=1

# video.release()
# cv2.destroyAllWindows()

rf = Roboflow(api_key="CPkBglSIfMhKhrghnYcq")
project = rf.workspace().project("dodgeball-detection")
model = project.version(1).model

for k in range(1000,1010):
    prediction = model.predict("/Users/efraimzetterqvist/Documents/dodge/dodge"+str(k)+'.jpg')
    print(prediction)

#print(prediction)
# infer on a local image
#print(model.predict("/Users/efraimzetterqvist/Library/Mobile Documents/com~apple~CloudDocs/Chalmers/haarpositiv/images-8.jpeg", confidence=40, overlap=30).json())