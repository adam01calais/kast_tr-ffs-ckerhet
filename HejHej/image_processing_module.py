import cv2
import os
from roboflow import Roboflow
import shutil

class ImageProcessing:

    def __init__(self, video_floor, video_side):
        self.video1 = cv2.VideoCapture(video_floor)
        self.video2 = cv2.VideoCapture(video_side)
        self.cross_position_x_1=[]
        self.cross_position_y_1=[]
        self.cross_position_x_2=[]
        self.cross_position_y_2=[]
        self.dodgeball_position_x=[]
        self.dodgeball_position_y=[]

    def detect(self, video_path, video_name, a, b):
        
        folder_name = "dodge"
        os.mkdir(os.path.join(video_path, folder_name))
        print(f"Created folder {folder_name} in directory {video_path}")

        x = []
        y = []
        w = []
        h = []

        video = cv2.VideoCapture(video_path + video_name)

        i=0
        path = video_path + "/" + folder_name 
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

        for k in range(a,b):
            prediction = model.predict(path + str(k) + '.jpg')
            for result in prediction.json()['predictions']:
                x.append(result['x'])
                y.append(result['y'])
                w.append(result['width'])
                h.append(result['height'])
        print(x, y, w, h)

        shutil.rmtree(path)

    #def calibrate_cross(self):

image=ImageProcessing("/Users/efraimzetterqvist/Library/Mobile Documents/com~apple~CloudDocs/Chalmers/IMG_1159 2.mov", "/Users/efraimzetterqvist/Library/Mobile Documents/com~apple~CloudDocs/Chalmers/IMG_1159 2.mov").detect("/Users/efraimzetterqvist/Library/Mobile Documents/com~apple~CloudDocs/Chalmers", "/IMG_1159.mov", 1, 5)




