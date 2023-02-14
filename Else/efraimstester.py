
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

from roboflow import Roboflow

rf = Roboflow(api_key="CPkBglSIfMhKhrghnYcq")
project = rf.workspace().project("dodgeball-detection")
model = project.version(1).model

x = []
y = []
w = []
h = []

for k in range(1000,1010):
    prediction = model.predict("/Users/efraimzetterqvist/Documents/dodge/dodge"+str(k)+'.jpg')
    for result in prediction.json()['predictions']:
        x.append(result['x'])
        y.append(result['y'])
        w.append(result['width'])
        h.append(result['height'])
print(x, y, w, h)

#print(prediction)
# infer on a local image
#print(model.predict("/Users/efraimzetterqvist/Library/Mobile Documents/com~apple~CloudDocs/Chalmers/haarpositiv/images-8.jpeg", confidence=40, overlap=30).json())