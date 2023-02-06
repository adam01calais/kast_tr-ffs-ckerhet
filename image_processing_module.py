from cv2 import cv2

class ImageProcessing:
    
    def __init__(self, video1, video2):
        self.video1 = video1
        self.video2 = video2
    def calibrate_cross(self):
        # Här håller vi en dodgeball mot krysset för att veta vad centrum är för krysset. 
        # Ville egentligen detektera krysset direkt, 
        # men verkar vara svårare än att detektera bollen av någon anledning, 
        # så därför använder jag mig av bollen för att kalibrera krysset
        dodgeball_cascade = cv2.CascadeClassifier('dodgeball.xml')
        cross_positions = []
        while True:
            ret1, frame1 = self.video1.read()
            ret2, frame2 = self.video2.read()
            gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            dodgeballs1 = dodgeball_cascade.detectMultiScale(gray1, 1.3, 5)
            dodgeballs2 = dodgeball_cascade.detectMultiScale(gray2, 1.3, 5)
            for (x,y,w,h) in dodgeballs1:
                #Gör en rektangel runt bollen och för in x-och y-koordinater för video1
                cv2.rectangle(frame1,(x,y),(x+w,y+h),(255,0,0),2)
                cross_positions.append((x, y))
            for (x,y,w,h) in dodgeballs2:
                #Gör en rektangel runt bollen och för in x-och y-koordinater för video2
                cv2.rectangle(frame2,(x,y),(x+w,y+h),(255,0,0),2)
                cross_positions.append((x, y))
            cv2.imshow('Video 1',frame1)
            cv2.imshow('Video 2',frame2)
            # Image processing av videon görs fram till dess att vi trycker på 'q'. 
            # Behöver definiera om när vi ska sluta mäta bollens position.
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.video1.release()
        self.video2.release()
        cv2.destroyAllWindows()
        # returns poitionen för bollen i förhållande till det vöre vänstra hörnet av kamerans synfält.
        return cross_positions

    def detect_dodgeball(self):
        # Använder en cascade classifier som är specificerad för att urskilja dodgeballs i bilder.
        dodgeball_cascade = cv2.CascadeClassifier('dodgeball.xml')
        positions = []
        while True:
            # ret1 och ret2 anger om videon var korrekt läst eller inte (True eller False)
            ret1, frame1 = self.video1.read()
            ret2, frame2 = self.video2.read()
            gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            dodgeballs1 = dodgeball_cascade.detectMultiScale(gray1, 1.3, 5)
            dodgeballs2 = dodgeball_cascade.detectMultiScale(gray2, 1.3, 5)
            for (x,y,w,h) in dodgeballs1:
                # Gör en rektangel runt bollen och för in x-och y-koordinater för video1
                # x och y är här utifrån det övre vänstra hörnet av videon.
                center_x = (x + (x + w)) / 2
                center_y = (y + (y + h)) / 2
                cv2.rectangle(frame1,(x,y),(x+w,y+h),(255,0,0),2)
                positions.append((center_x, center_y))
            for (x,y,w,h) in dodgeballs2:
                # Gör en rektangel runt bollen och för in x-och y-koordinater för video2
                # x och y är här utifrån det övre vänstra hörnet av videon.
                center_x = (x + (x + w)) / 2
                center_y = (y + (y + h)) / 2
                cv2.rectangle(frame1,(x,y),(x+w,y+h),(255,0,0),2)
                positions.append((center_x, center_y))
            # Tror de här två raderna visar upp den specifika framen. Är en ganska cool funktion att visa 
            # upp den exakta bilden då bollen träffar väggen i appen. Eventuellt
            cv2.imshow('Video 1',frame1)
            cv2.imshow('Video 2',frame2)
            # Här vill vi istället att loopen ska breaka om bollen har nått det plan som är parallellt
            # med väggen och går genom centrum av kalibreringsbollen, dvs når 'cross_positions' i 
            # 'calibrate_cross'. 
            # Behöver alltså få in infon från den metoden till denna.
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.video1.release()
        self.video2.release()
        cv2.destroyAllWindows()
        # returns poitionen för bollens centrum i förhållande till det vöre vänstra hörnet av 
        # kamerornas synfält.
        return positions

    