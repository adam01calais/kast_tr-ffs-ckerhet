import cv2
import os
from roboflow import Roboflow
import shutil


video_name= "calibration.mov"
directory_path = "C:/Users/Joakim/Documents/3an/Kandidatarbete/Egen programmering"
folder_name = "dodge"

def calibration(directory_path,video_name):
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


    #Vill skapa en lista med bilder under tre sekunder med hopp om frame_rate genom tre
    frame_rate_by_three=frame_rate/3
    frame_rate_times_three=frame_rate*3
    list_of_images_numbers=list(range(1,int(frame_rate_times_three),int(frame_rate_by_three)))


    for k in list_of_images_numbers:
        prediction = model.predict(directory_path + "/" + folder_name + "/dodge" + str(k) + '.jpg')
        for result in prediction.json()['predictions']:
            x.append(result['x'])
            y.append(result['y'])
        if len(x) < 2:
            continue
        if len(y) < 2:
            continue
        if max(abs(x[-2] - x[-1]), abs(y[-2] - y[-1])) < 5:
            print('Calibration for camera done successfully')
            break
    shutil.rmtree(directory_path + '/' + folder_name) 

    print(x[-1],y[-1])


cross_x=380.0
cross_y=482.0

def measure_throw(directory_path,video_name,cross_x,cross_y):






