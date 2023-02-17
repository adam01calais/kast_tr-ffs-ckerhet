import cv2
import os
from roboflow import Roboflow


x = []
y = []
w = []
h = []


video_name= "IMG_4550.mov"
directory_path = "C:/Users/Joakim/Documents/3an/Kandidatarbete/Egen programmering"
folder_name = "dodge"

folder_name = "dodge"
os.mkdir(os.path.join(directory_path, folder_name))
print(f"Created folder {folder_name} in directory {directory_path}")


video = cv2.VideoCapture(directory_path+ "/"+video_name)

i=0
while(video.isOpened()):
    ret, frame = video.read()
    if ret == False:
        break
    cv2.imwrite(os.path.join(directory_path+"/"+"dodge",'dodge'+str(i)+'.jpg'),frame)
    i+=1
video.release()
cv2.destroyAllWindows()


rf = Roboflow(api_key="CPkBglSIfMhKhrghnYcq")
project = rf.workspace().project("dodgeball-detection")
model = project.version(1).model

list_of_images_numbers=range(1,3,10)

for k in list_of_images_numbers:
    prediction = model.predict(directory_path+"/dodge/"+"/dodge" + str(k) + '.jpg')
    for result in prediction.json()['predictions']:
        x.append(result['x'])
        y.append(result['y'])
        w.append(result['width'])
        h.append(result['height'])
print(x, y, w, h)



