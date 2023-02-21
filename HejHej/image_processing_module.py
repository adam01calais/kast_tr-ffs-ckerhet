import cv2
import os
from roboflow import Roboflow
import shutil

class ImageProcessing:

    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.folder_name = "dodge"
    
    def calibrate_cross(self, video_path, camera_angle):

        # Skapar den tomma mappen 'dodge' på plats vald av användaren
        os.mkdir(os.path.join(self.directory_path, self.folder_name))
        print(f"Created folder {self.folder_name} in directory {self.directory_path}")

        # Öppnar kalibreringsvideon
        video = cv2.VideoCapture(video_path)

        # Delar upp videon i frames som placeras i mappen 'dodge'
        i=0
        path = self.directory_path + "/" + self.folder_name
        while(video.isOpened()):
            ret, frame = video.read()
            if ret == False:
                break
            cv2.imwrite(os.path.join(path,'dodge'+str(i)+'.jpg'),frame)
            i+=1
        frame_rate = int(video.get(cv2.CAP_PROP_FPS))

        # Stänger ner videon
        video.release()
        cv2.destroyAllWindows()

        # Tillkallar en i Roboflow tränad modell för att detektera fotbollar
        rf = Roboflow(api_key="CPkBglSIfMhKhrghnYcq")
        project = rf.workspace().project("dodgeball-detection")
        model = project.version(1).model

        # Gör en lista över de frames där detektering av dodgeball är aktuell för kalibrering
        list_of_images_numbers = list(range(1, i, frame_rate))

        # Skapar listor för bildens x- & y-koordinat
        x = []
        y = []

        # Detekterar bollen för de aktuella framesen och stoppar kalibreringen då 
        # då bollen varit relativt stilla mellan två aktuella frames (1 sekund)
        for k in list_of_images_numbers:
            prediction = model.predict(self.directory_path + "/" + self.folder_name + "/dodge" + str(k) + '.jpg')
            for result in prediction.json()['predictions']:
                x.append(result['x'])
                y.append(result['y'])
            if len(x) < 2:
                continue
            if len(y) < 2:
                continue
            if max(abs(x[-2] - x[-1]), abs(y[-2] - y[-1])) < 3:
                print('Calibration for ' + camera_angle + ' camera done successfully')
                break
        
        # Sparar kryssets x- & y-koordinat i två variabler 
        cross_position_x = x[-1]
        cross_position_y = y[-1]

        # Raderar mappen 'dodge' innehållandes alla frames
        shutil.rmtree(self.directory_path + '/' + self.folder_name)  

        # Skriver ut kryssets koordinater samt returnerar dem
        print('x: ' + str(cross_position_x), 'y: ' + str(cross_position_y))  
        return cross_position_x, cross_position_y   

    def measure_throw(self, video_path, camera_angle):

        # Skapar den tomma mappen 'dodge' på plats vald av användaren
        os.mkdir(os.path.join(self.directory_path, self.folder_name))
        print(f"Created folder {self.folder_name} in directory {self.directory_path}")

        # Öppnar kastvideon
        video = cv2.VideoCapture(video_path)

        # Delar upp videon i frames som placeras i mappen 'dodge'
        i=0
        path = self.directory_path + "/" + self.folder_name
        while(video.isOpened()):
            ret, frame = video.read()
            if ret == False:
                break
            cv2.imwrite(os.path.join(path,'dodge'+str(i)+'.jpg'),frame)
            i+=1

        # Stänger ner videon
        video.release()
        cv2.destroyAllWindows()

        # Tillkallar en i Roboflow tränad modell för att detektera fotbollar
        rf = Roboflow(api_key="CPkBglSIfMhKhrghnYcq")
        project = rf.workspace().project("dodgeball-detection")
        model = project.version(1).model

        # Skapar listor för bildens x- & y-koordinat
        x = []
        y = []

        for k in range(1,i):
            prediction = model.predict(self.directory_path + "/" + self.folder_name + "/dodge" + str(k) + '.jpg')
            for result in prediction.json()['predictions']:
                x.append(result['x'])
                y.append(result['y'])
            print(x, y)
            k+=1
            if len(x) < 2:
                continue
            if len(y) < 2:
                continue
            if x[-1] > x[-2]:
                print('Throw for ' + camera_angle + ' successfully measured')
                break

        # Raderar mappen 'dodge' innehållandes alla frames
        shutil.rmtree(self.directory_path + '/' + self.folder_name)  

        # Skriver ut bollens koordinater i varje frame fram tills att den träffar väggen
        # och returnerar dem i en lista för x och en för y. Den frame då bollen först kommer in i bild 
        # ger det första elementet i listan och därmed är den sista framen det sista elementet i listan.
        print('Bollens positioner i x: ' + x, 'Bollens position i y: ' + y)  
        return x, y 