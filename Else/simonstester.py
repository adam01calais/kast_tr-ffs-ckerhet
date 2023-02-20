import cv2
import os
from roboflow import Roboflow
import shutil


video_name_calibration= "calibration.mov"
video_name_slowmotion="slowmotion.mov"
directory_path = "C:/Users/Joakim/Documents/3an/Kandidatarbete/Egen programmering"
folder_name = "dodge"

def measure_throw(directory_path,video_name):
    x = []
    y = []

    folder_name = "dodge"
    os.mkdir(os.path.join(directory_path, folder_name))
    print(f"Created folder {folder_name} in directory {directory_path}")

    video = cv2.VideoCapture(directory_path+ "/"+video_name)
    frame_rate = int(video.get(cv2.CAP_PROP_FPS))

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


    a=1
    while True:
        list_of_images_numbers=list(range(a,i))

        for k in list_of_images_numbers:
            print(k)
            prediction = model.predict(directory_path + "/" + folder_name + "/dodge" + str(k) + '.jpg')
            for result in prediction.json()['predictions']:
                x.append(result['x'])
                y.append(result['y'])
            if len(x) == 0 or len(y)==0:
                a+=20 #Hur många frames som ska hoppas över
                break

    print(x,y)

    shutil.rmtree(directory_path + '/' + folder_name) 




measure_throw(directory_path,video_name_slowmotion)


