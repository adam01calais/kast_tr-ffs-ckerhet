import numpy as np
from scipy.optimize import curve_fit
import math

class DataAnalysis:
    # Input: bollens poition för kamera 1 och 2
    def __init__(self, dodgeball_position_x, dodgeball_position_y, dodgeball_diameter, 
        image_width_x, image_width_y, distance_camera_x, distance_camera_y, focal_length_x, focal_length_y):
        self.dodgeball_position_x = dodgeball_position_x
        self.dodgeball_position_y = dodgeball_position_y
        self.dodgeball_diameter = dodgeball_diameter
        self.image_width_x = image_width_x      # width of the video frame in pixels
        self.image_width_y = image_width_y      # width of the video frame in pixels
        self.distance_camera_x = distance_camera_x
        self.distance_camera_y = distance_camera_y
        self.focal_length_x = focal_length_x    # distance between the lens and the image sensor in meters camera x
        self.focal_length_y = focal_length_y    # distance between the lens and the image sensor in meters camera y


    # Curve fitting is a type of optimization that finds an optimal set of parameters for a defined function that best fits a given set of observations.
   # Får in en lista med positioner där bollen har varit varje frame/second, en lista för x och en för y
    def calculate_velocity(self):
        time = np.linspace(0, len(self.dodgeball_position_x), len(self.dodgeball_position_y))
        velocity1, _ = curve_fit(lambda t, a, b: a*t + b,  time, self.dodgeball_position_x)
        velocity2, _ = curve_fit(lambda t, a, b: a*t + b,  time, self.dodgeball_position_y)
        return velocity1[0], velocity2[0]
    
        
    # Får in x- och y-koordinat när bollen hamnade (cross_position x och y)
    def calculate_accuracy(self, cross_position_x, cross_position_y):
        # Hur fel bollen hamnade i x- och y-led mätt i pixlar
        x_error_pixels = cross_position_x - self.dodgeball_position_x[-1] # sista elementet
        y_error_pixels = cross_position_y - self.dodgeball_position_y[-1]

        # Behöver konverteras till cm (kanske?) eller annan längdenhet
        # pixels_per_meter = video_frame_width / field_of_view_width_in_meters
        # Measure the distance between the camera and the object in meters

        pixel_size_x = (self.dodgeball_diameter / self.image_width_x) * (self.distance_camera_x * self.focal_length_x)
        pixel_size_y = (self.dodgeball_diameter / self.image_width_y) * (self.distance_camera_y * self.focal_length_y)
       
        x = x_error_pixels * pixel_size_x
        y = y_error_pixels * pixel_size_y
       
        accuracy = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
        
        return (accuracy)
    
