import pyicloud
from pyicloud import PyiCloudService

class CameraControl:
    #device1 = PyiCloudService("username1", "password1")
    #username och password för icloud
    def __init__(self, device1, device2):
        self.device1 = device1
        self.device2 = device2

    def start_recording(self):
        self.device1.start_recording()
        self.device2.start_recording()

    def stop_recording(self):
        self.device1.stop_recording()
        self.device2.stop_recording()
        
    def set_resolution(self, resolution):
        self.device1.set_resolution(resolution)
        self.device2.set_resolution(resolution)

    def set_frame_rate(self, frame_rate):
        self.device1.set_frame_rate(frame_rate)
        self.device2.set_frame_rate(frame_rate)

