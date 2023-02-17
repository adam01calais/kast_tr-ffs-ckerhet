import cv2
import os
from roboflow import Roboflow
import shutil

class ImageProcessing:

    def __init__(self, directory_path):
        #self.video_floor_path = video_floor_path # cv2.VideoCapture(video_floor)
        #self.video_side_path = video_side_path # cv2.VideoCapture(video_side)
        self.directory_path = directory_path
        self.folder_name = "dodge"
        #self.folder_name_side = "dodge_side"
        self.cross_position_x_floor = 0
        self.cross_position_y_floor = 0
        self.cross_position_x_side = 0
        self.cross_position_y_side = 0
        self.dodgeball_position_x=[]
        self.dodgeball_position_y=[]
    
    def calibrate_cross(self, video_path, camera_angle):

        os.mkdir(os.path.join(self.directory_path, self.folder_name))
        print(f"Created folder {self.folder_name} in directory {self.directory_path}")

        video = cv2.VideoCapture(video_path)

        i=0
        path = self.directory_path + "/" + self.folder_name
        while(video.isOpened()):
            ret, frame = video.read()
            if ret == False:
                break
            cv2.imwrite(os.path.join(path,'dodge'+str(i)+'.jpg'),frame)
            i+=1
        frame_rate = int(video.get(cv2.CAP_PROP_FPS))
        frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video.release()
        cv2.destroyAllWindows()

        rf = Roboflow(api_key="CPkBglSIfMhKhrghnYcq")
        project = rf.workspace().project("dodgeball-detection")
        model = project.version(1).model

        list_of_images_numbers = list(range(1, frame_rate*100, frame_rate))

        x = []
        y = []
        w = []
        h = []

        for k in list_of_images_numbers:
            prediction = model.predict(self.directory_path + "/" + self.folder_name + "/dodge" + str(k) + '.jpg')
            for result in prediction.json()['predictions']:
                x.append(result['x'])
                y.append(result['y'])
                w.append(result['width'])
                h.append(result['height'])
            print(k, x, y)
            if len(x) < 2:
                print('x för liten')
                continue
            if len(y) < 2:
                print('y för liten')
                continue
            if max(abs(x[-2] - x[-1]), abs(y[-2] - y[-1])) < 4:
                print('calibration_coordinates: ', x, y)
                print('Calibration for ' + camera_angle + ' camera done successfully')
                break
        self.cross_position_x = x[-1]
        self.cross_position_y = y[-1]

        shutil.rmtree(self.directory_path + '/' + self.folder_name)  
        print(self.cross_position_x, self.cross_position_y)  
        return self.cross_position_x, self.cross_position_y   

            
image=ImageProcessing("/Users/efraimzetterqvist/Documents") 
cross_floor=image.calibrate_cross('/Users/efraimzetterqvist/Documents/IMG_1160.mov', 'floor')
cross_side=image.calibrate_cross("/Users/efraimzetterqvist/Documents/IMG_1179.mov", 'side')
