import subprocess
import pyicloud
from pyicloud import PyiCloudService

class CameraControl:
# The device1 and device2 input arguments should be dictionaries containing information about the devices, 
# including the platform ("ios" or "android"), username and password for iOS devices, 
# and device ID for Android devices.
    def __init__(self, device1, device2):
        self.device1 = device1
        self.device2 = device2

    def start_recording(self):
        if self.device1["platform"] == "ios":
            icloud = PyiCloudService(self.device1["username"], self.device1["password"])
            icloud.start_recording()
        else:
            subprocess.call(["adb", "-s", self.device1["device_id"], "shell", "screenrecord", "--time-limit", "10", "/sdcard/test.mp4"])

        if self.device2["platform"] == "ios":
            icloud = PyiCloudService(self.device2["username"], self.device2["password"])
            icloud.start_recording()
        else:
            subprocess.call(["adb", "-s", self.device2["device_id"], "shell", "screenrecord", "--time-limit", "10", "/sdcard/test.mp4"])
            
    def stop_recording(self):
        if self.device1["platform"] == "ios":
            icloud = PyiCloudService(self.device1["username"], self.device1["password"])
            icloud.stop_recording()
        else:
            subprocess.call(["adb", "-s", self.device1["device_id"], "shell", "pkill", "screenrecord"])

        if self.device2["platform"] == "ios":
            icloud = PyiCloudService(self.device2["username"], self.device2["password"])
            icloud.stop_recording()
        else:
            subprocess.call(["adb", "-s", self.device2["device_id"], "shell", "pkill", "screenrecord"])


