import cv2
import os
from roboflow import Roboflow
import shutil
from data_analysis_module_2 import DataAnalyzis 

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
        rf = Roboflow(api_key="koGvCT0SUYgs5aM6SvHp")
        project = rf.workspace().project("dodgeball-detection-pcb7n")
        model = project.version(1).model

        # Gör en lista över de frames där detektering av dodgeball är aktuell för kalibrering
        list_of_images_numbers = list(range(1, i, frame_rate))

        # Skapar listor för bildens x- & y-koordinat
        x = []
        y = []
        w = []
        h = []

        # Detekterar bollen för de aktuella framesen och stoppar kalibreringen då 
        # då bollen varit relativt stilla mellan två aktuella frames (1 sekund)
        for k in list_of_images_numbers:
            prediction = model.predict(self.directory_path + "/" + self.folder_name + "/dodge" + str(k) + '.jpg')
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
                print('Calibration for ' + camera_angle + ' camera done successfully')
                break
        
        # Sparar kryssets x- & y-koordinat i två variabler 
        cross_position_x = x[-1]
        cross_position_y = y[-1]
        self.ball_radius = (w[-1] + h[-1])/4

        # Raderar mappen 'dodge' innehållandes alla frames
        shutil.rmtree(self.directory_path + '/' + self.folder_name)  

        # Skriver ut kryssets koordinater samt returnerar dem
        print('x: ' + str(cross_position_x), 'y: ' + str(cross_position_y))  
        print('Bollens radie för ' + camera_angle + ' camera: ' + str(self.ball_radius))
        return cross_position_x, cross_position_y, self.ball_radius

    def measure_throw(self, video_path, min_ball_area, camera_angle):

        # Öppnar kastvideon
        video = cv2.VideoCapture(video_path)
        fps = int(video.get(cv2.CAP_PROP_FPS))

        # Extract the first frame as the background image
        _, bg = video.read()
        bg_gray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)

        # Define the threshold for detecting the ball
        threshold = 6

        # Skapar listor för bildens x- & y-koordinat
        x_list = []
        y_list = []
        w_list = []
        h_list = []

        count = 0

        radius = int(self.ball_radius)

        while(video.isOpened()):
            ret, frame = video.read()
            if ret == False:
                break
            # Convert the current frame to grayscale
            count += 1
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Subtract the background from the current frame
            diff = cv2.absdiff(bg_gray, frame_gray)

            # Apply a threshold to the difference image
            _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

            # Apply morphological operations to remove noise
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            thresh = cv2.erode(thresh, kernel, iterations=2)
            thresh = cv2.dilate(thresh, kernel, iterations=2)

            # Find contours in the binary image
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Loop through the contours
            for contour in contours:
                # Calculate the area of the contour
                area = cv2.contourArea(contour)

                # If the area is larger than the minimum area, it is likely a ball
                if area > min_ball_area:
                    # Draw a bounding box around the ball
                    x, y, w, h = cv2.boundingRect(contour)
                    center_x = x + w/2
                    center_y = y + h/2
                    x_list.append(center_x)
                    y_list.append(center_y)
                    w_list.append(w)
                    h_list.append(h)
                    box_left_corner_x = int(center_x - radius)
                    box_left_corner_y = int(center_y + radius)
                    box_right_corner_x = int(center_x + radius)
                    box_right_corner_y = int(center_y - radius)
                    cv2.rectangle(frame, (box_left_corner_x, box_left_corner_y), (box_right_corner_x, box_right_corner_y), (0, 0, 255), 2)
                    break
            
            # Display the current frame
            cv2.imshow('frame', frame)
            if camera_angle == 'side':
                if len(x_list) < count:
                    x_list.append(0)
                    y_list.append(0)
                    w_list.append(0)
                    h_list.append(0)
                if len(x_list) < 2:
                    continue
            
                if x_list[-1] < x_list[-2]:
                    if x_list[-1] == 0:
                        continue
                    else:
                        del x_list[-1:]
                        del y_list[-1:]
                        del w_list[-1:]
                        del h_list[-1:]
                        break
                
            if camera_angle == 'floor':

                if len(y_list) < count:
                    x_list.append(0)
                    y_list.append(0)
                    w_list.append(0)
                    h_list.append(0)

                if len(y_list) < 2:
                    continue
            
                if y_list[-1] > y_list[-2]:
                    if y_list[-2] == 0:
                        continue
                    else:
                        del x_list[-1:]
                        del y_list[-1:]
                        del w_list[-1:]
                        del h_list[-1:]
                        break

            # Check for key press
            key = cv2.waitKey(100)
            if key == ord('q'):
                break

        # Stänger ner videon
        video.release()
        cv2.destroyAllWindows() 

        # print(x_list)
        # print(y_list)
        # print(w_list)
        # print(h_list)

        # Skriver ut bollens koordinater i varje frame fram tills att den träffar väggen
        # och returnerar dem i en lista för x och en för y. Den frame då bollen först kommer in i bild 
        # ger det första elementet i listan och därmed är den sista framen det sista elementet i listan.
        print('Bollens position för ' + camera_angle + ' camera i x-led: ' + str(x_list))
        print('Bollens position för ' + camera_angle + ' camera i y-led: ' + str(y_list))  
        return x_list, y_list, fps


object = ImageProcessing('/Users/efraimzetterqvist/Documents')

cal_floor_x, cal_floor_y, ball_radius_floor = object.calibrate_cross('/Users/efraimzetterqvist/Documents/IMG_1160.mov', 'floor')
cal_side_x, cal_side_y, ball_radius_side = object.calibrate_cross('/Users/efraimzetterqvist/Documents/IMG_1159.mov', 'side')
throw_floor_x, throw_floor_y, fps_floor = object.measure_throw('/Users/efraimzetterqvist/Documents/IMG_1165.mov', 1/3*(ball_radius_floor*2)**2, 'floor')
throw_side_x, throw_side_y, fps_side = object.measure_throw('/Users/efraimzetterqvist/Documents/IMG_1161.mov', 1/3*(ball_radius_side*2)**2, 'side')
throw = DataAnalyzis(throw_floor_x, throw_floor_y, throw_side_x, throw_side_y, fps_side, ball_radius_floor, ball_radius_side)
throw_velocity = throw.velocity()
throw_accuracy = throw.accuracy(cal_floor_x, cal_floor_y, cal_side_x, cal_side_y)
