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

    def detect(self, directory_path, video_name, list_of_images_numbers):

        video_name= "IMG_1159 2.mov"
        directory_path = "/Users/efraimzetterqvist/Documents"

        folder_name = "dodge"
        os.mkdir(os.path.join(directory_path, folder_name))
        print(f"Created folder {folder_name} in directory {directory_path}")

        x = []
        y = []
        w = []
        h = []

<<<<<<< HEAD

        video=cv2.VideoCapture(directory_path+"/"+video_name)
=======
        video = cv2.VideoCapture(video_path + "/" + video_name)
>>>>>>> ab475a4c176c2564a742aa7be74a82d0133f4189

        i=0
        path= directory_path + "/" + folder_name
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

        for k in list_of_images_numbers:
            prediction = model.predict(path+"/dodge" + str(k) + '.jpg')
            for result in prediction.json()['predictions']:
                x.append(result['x'])
                y.append(result['y'])
                w.append(result['width'])
                h.append(result['height'])
        print(x, y, w, h)

<<<<<<< HEAD
        shutil.rmtree(path)       
    
    def calibrate_cross(self):
        cross_position_x=[]
        cross_position_y=[]
        frames_per_second='webscraping'
        
=======
        shutil.rmtree(path)

    #def calibrate_cross(self):

image=ImageProcessing("/Users/efraimzetterqvist/Documents/IMG_1159 2.mov", "/Users/efraimzetterqvist/Documents/IMG_1159 2.mov").detect("/Users/efraimzetterqvist/Documents", "IMG_1159 2.mov", 1, 5)
>>>>>>> ab475a4c176c2564a742aa7be74a82d0133f4189



        i=range()

        while True:

            