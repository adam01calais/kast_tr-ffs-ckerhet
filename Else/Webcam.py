import cv2
import time
import datetime

cap = cv2.VideoCapture(0)

path="C:/Users/Joakim/Documents/3an/Kandidatarbete/Egen programmering/Webcamtest"

frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S-%f")
out = cv2.VideoWriter(path+"/"+current_time+".mp4", fourcc, 30.0, frame_size)


while True: 
        _, frame = cap.read()

        out.write(frame)

        cv2.imshow("Camera", frame)

        if cv2.waitKey(1) == ord('q'):
             break
        
        
out.release()       
cap.release()
cv2.destroyAllWindows()


        

        