import cv2
import os
from roboflow import Roboflow
import shutil
import numpy as np

def calibrate_cross(video_path):

        # Skapar den tomma mappen 'dodge' på plats vald av användaren
        os.mkdir('/Users/efraimzetterqvist/Documents/dodge')
        print(f"Created folder dodge")

        # Öppnar kalibreringsvideon
        video = cv2.VideoCapture(video_path)

        # Delar upp videon i frames som placeras i mappen 'dodge'
        i=0
        path = '/Users/efraimzetterqvist/Documents/dodge'
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
        rf = Roboflow(api_key="HEfNlI5lkTBazBknN8jz")
        project = rf.workspace().project("footballs-1trlz")
        model = project.version(3).model

        # Gör en lista över de frames där detektering av dodgeball är aktuell för kalibrering
        list_of_images_numbers = list(range(1, i, frame_rate))

        # Skapar listor för bildens x- & y-koordinat och bollens bredd och höjd
        x = []
        y = []
        w = []
        h = []

        # Detekterar bollen för de aktuella framesen och stoppar kalibreringen då 
        # bollen varit relativt stilla mellan två aktuella frames (1 sekund)
        for k in list_of_images_numbers:
            prediction = model.predict('/Users/efraimzetterqvist/Documents/dodge' + "/dodge" + str(k) + '.jpg')
            for result in prediction.json()['predictions']:
                x.append(result['x'])
                y.append(result['y'])
                w.append(result['width'])
                h.append(result['height'])
            if len(x) < 2:
                continue
            if len(y) < 2:
                continue
            if max(abs(x[-2] - x[-1]), abs(y[-2] - y[-1])) < 3:
                print('Calibration for camera done successfully')
                break
        # Om bollen inte kunde detekteras
        if len(x) == 0:
            # Raderar mappen 'dodge' innehållandes alla frames
            shutil.rmtree('/Users/efraimzetterqvist/Documents/dodge') 
            return None, None, None
        else: 
            # Sparar kryssets x- & y-koordinat i två variabler samt bollens radie
            cross_position_x = x[-1]
            cross_position_y = y[-1]
            ball_radius = (w[-1] + h[-1])/4

            # Raderar mappen 'dodge' innehållandes alla frames
            shutil.rmtree('/Users/efraimzetterqvist/Documents/dodge')  

            # Skriver ut kryssets koordinater samt returnerar dem + bollens radie
            print('x: ' + str(cross_position_x), 'y: ' + str(cross_position_y))  
            print('Bollens radie för camera: ' + str(ball_radius))
            return cross_position_x, cross_position_y, ball_radius