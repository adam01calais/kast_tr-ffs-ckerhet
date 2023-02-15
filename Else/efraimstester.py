
import cv2
import os
from roboflow import Roboflow
import shutil

folder_name = "dodge"
directory_path = "/Users/efraimzetterqvist/Documents"
os.mkdir(os.path.join(directory_path, folder_name))
print(f"Created folder {folder_name} in directory {directory_path}")

x = []
y = []
w = []
h = []

video=cv2.VideoCapture("/Users/efraimzetterqvist/Library/Mobile Documents/com~apple~CloudDocs/Chalmers/IMG_1159 2.mov")

i=0
path= directory_path + "/" + folder_name # "/Users/efraimzetterqvist/Documents/dodge"
while(video.isOpened()):
    ret, frame = video.read()
    if ret == False:
        break
    cv2.imwrite(os.path.join(path,'dodge'+str(i)+'.jpg'),frame)
    i+=1
video.release()
cv2.destroyAllWindows()

rf = Roboflow(api_key="CPkBglSIfMhKhrghnYcq")
project = rf.workspace().project("dodgeball-detection")
model = project.version(1).model

for k in range(1,5):
    prediction = model.predict("/Users/efraimzetterqvist/Documents/dodge/dodge" + str(k) + '.jpg')
    for result in prediction.json()['predictions']:
        x.append(result['x'])
        y.append(result['y'])
        w.append(result['width'])
        h.append(result['height'])
print(x, y, w, h)

shutil.rmtree(path)