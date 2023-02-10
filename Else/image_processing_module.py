import cv2
import time

class ImageProcessing:
    
    # video1 (Kameran från sidan)
    # video2 (Kameran underifrån)
    def __init__(self, video1, video2):
        self.video1 = cv2.VideoCapture(video1)
        self.video2 = cv2.VideoCapture(video2)
        self.cross_position_x_1=[]
        self.cross_position_y_1=[]
        self.cross_position_x_2=[]
        self.cross_position_y_2=[]
        self.dodgeball_position_x=[]
        self.dodgeball_position_y=[]

    def calibrate_cross(self):
        ball_stationary = False
        start_time = time.time()
        dodgeball_cascade = cv2.CascadeClassifier('dodgeball.xml')
        cross_position_x_1=[]
        cross_position_y_1=[]
        cross_position_x_2=[]
        cross_position_y_2=[]

        while not ball_stationary:
            # code to track the ball's movement
            current_time = time.time()
            ret1, frame1 = self.video1.read()
            ret2, frame2 = self.video2.read()
            gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            dodgeballs1 = dodgeball_cascade.detectMultiScale(gray1, 1.3, 5)
            dodgeballs2 = dodgeball_cascade.detectMultiScale(gray2, 1.3, 5)
            for (x,y,w,h) in dodgeballs1:
                center_x_1 = (x + (x + w)) / 2
                center_y_1 = (y + (y + h)) / 2
                # Gör en rektangel runt bollen och för in x-och y-koordinater för video1
                cv2.rectangle(frame1,(x,y),(x+w,y+h),(255,0,0),2)
                cross_position_x_1.append(center_x_1)
                cross_position_y_1.append(center_y_1)
            for (x,y,w,h) in dodgeballs2:
                center_x_2 = (x + (x + w)) / 2
                center_y_2 = (y + (y + h)) / 2
                #G ör en rektangel runt bollen och för in x-och y-koordinater för video2
                cv2.rectangle(frame2,(x,y),(x+w,y+h),(255,0,0),2)
                cross_position_x_2.append(center_x_2)
                cross_position_y_2.append(center_y_2)

            if len(cross_position_x_1) or len(cross_position_y_1) or len(cross_position_x_2) or len(cross_position_y_2) < 2:
                continue

            change = max(abs(cross_position_x_1[-1] - cross_position_x_1[-2]), abs(cross_position_y_1[-1] - cross_position_y_1[-2]), abs(cross_position_x_2[-1] - cross_position_x_2[-2]), abs(cross_position_y_2[-1] - cross_position_y_2[-2]))
            if change < 10:  # if the change in position is less than 10 pixels
                time_stationary = current_time - start_time
                if time_stationary >= 4:
                    ball_stationary = True
                    cross_position_x_1=cross_position_x_1[-1]
                    cross_position_y_1=cross_position_y_1[-1]
                    cross_position_x_2=cross_position_x_2[-1]
                    cross_position_y_2=cross_position_y_2[-1]
                    break
            else:
                start_time = current_time

            cv2.imshow('Video 1',frame1)
            cv2.imshow('Video 2',frame2)
        
        self.video1.release()
        self.video2.release()
        cv2.destroyAllWindows()
        
        self.cross_position_x_1=cross_position_x_1
        self.cross_position_x_2=cross_position_x_2
        self.cross_position_y_1=cross_position_y_1
        self.cross_position_y_2=cross_position_y_2

    def detect_dodgeball(self):
        # Använder en cascade classifier som är specificerad för att urskilja dodgeballs i bilder.
        # Behöver göra 'dodgeball.xml' själva
        dodgeball_cascade = cv2.CascadeClassifier('dodgeball.xml')
        dodgeball_position_x_1 = []
        dodgeball_position_x_2 = []
        dodgeball_position_y_1 = []
        dodgeball_position_y_2 = []
        while True:
            # ret1 och ret2 anger om videon var korrekt läst eller inte (True eller False)
            ret1, frame1 = self.video1.read()
            ret2, frame2 = self.video2.read()
            gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            dodgeballs1 = dodgeball_cascade.detectMultiScale(gray1, 1.3, 5)
            dodgeballs2 = dodgeball_cascade.detectMultiScale(gray2, 1.3, 5)

            if len(dodgeball_position_x_1) or len(dodgeball_position_y_2) < 1:
                continue

            if dodgeball_position_x_1[-1]>=self.cross_position_x_1:
                continue

            else:
                for (x,y,w,h) in dodgeballs1:
                    # x och y är här utifrån det övre vänstra hörnet av videon.
                    center_y_1 = (y + (y + h)) / 2
                    # Gör en rektangel runt bollen och för in x-och y-koordinater för video1
                    cv2.rectangle(frame1,(x,y),(x+w,y+h),(255,0,0),2)
                    dodgeball_position_y_1.append(center_y_1)

            if dodgeball_position_y_2[-1]>=self.cross_position_y_2:
                continue
            else:
                for (x,y,w,h) in dodgeballs2:
                    # x och y är här utifrån det övre vänstra hörnet av videon.
                    center_x_2 = (x + (x + w)) / 2
                    # Gör en rektangel runt bollen och för in x-och y-koordinater för video2
                    cv2.rectangle(frame1,(x,y),(x+w,y+h),(255,0,0),2)
                    dodgeball_position_x_2.append(center_x_2)
            # Tror de här två raderna visar upp den specifika framen. Är en ganska cool funktion att visa 
            # upp den exakta bilden då bollen träffar väggen i appen. Eventuellt
            cv2.imshow('Video 1',frame1)
            cv2.imshow('Video 2',frame2)
            # Här vill vi istället att loopen ska breaka om bollen har nått det plan som är parallellt
            # med väggen och går genom centrum av kalibreringsbollen, dvs når 'cross_positions' i 
            # 'calibrate_cross'. 
            # Behöver alltså få in infon från den metoden till denna.
            if dodgeball_position_x_1[-1]>=self.cross_position_x_1 and dodgeball_position_y_2[-1]>=self.cross_position_y_2:
                break
        self.video1.release()
        self.video2.release()
        cv2.destroyAllWindows()
        # returns poitionen för bollens centrum i förhållande till det vöre vänstra hörnet av 
        # kamerornas synfält.
        self.dodgeball_position_x = dodgeball_position_x_2
        self.dodgeball_position_y = dodgeball_position_y_1
        return self.dodgeball_position_x, self.dodgeball_position_y

