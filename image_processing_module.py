import cv2

class ImageProcessing:
    #video1 = cv2.VideoCapture("path/to/video1.mov")
    #Kan ändra variabeln till en path till filen istället
    #Kanske göra en till funktion här som enbart detekterar kryssets position
    def __init__(self, video1, video2):
        self.video1 = video1
        self.video2 = video2

    def detect_dodgeball(self):
        dodgeball_cascade = cv2.CascadeClassifier('dodgeball.xml')
        positions = []
        while True:
            ret1, frame1 = self.video1.read()
            ret2, frame2 = self.video2.read()
            gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            dodgeballs1 = dodgeball_cascade.detectMultiScale(gray1, 1.3, 5)
            dodgeballs2 = dodgeball_cascade.detectMultiScale(gray2, 1.3, 5)
            for (x,y,w,h) in dodgeballs1:
                cv2.rectangle(frame1,(x,y),(x+w,y+h),(255,0,0),2)
                positions.append((x, y))
            for (x,y,w,h) in dodgeballs2:
                cv2.rectangle(frame2,(x,y),(x+w,y+h),(255,0,0),2)
                positions.append((x, y))
            cv2.imshow('Video 1',frame1)
            cv2.imshow('Video 2',frame2)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.video1.release()
        self.video2.release()
        cv2.destroyAllWindows()
        return positions