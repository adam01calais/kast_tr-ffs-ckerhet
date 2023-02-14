import numpy as np
from scipy.optimize import curve_fit

class DataAnalysis:
    # Input: bollens poition för kamera 1 och 2
    def __init__(self, dodgeball_position_x, dodgeball_position_y):
        self.dodgeball_position_x = dodgeball_position_x
        self.dodgeball_position_y = dodgeball_position_y

    # Curve fitting is a type of optimization that finds an optimal set of parameters for a defined function that best fits a given set of observations.
   # Får in en lista med positioner där bollen har varit varje frame/second, en lista för x och en för y
    def calculate_velocity(self):
        time = np.linspace(0, len(self.dodgeball_position_x), len(self.dodgeball_position_y))
        velocity1, _ = curve_fit(lambda t, a, b: a*t + b,  time, self.dodgeball_position_x)
        velocity2, _ = curve_fit(lambda t, a, b: a*t + b,  time, self.dodgeball_position_y)
        return velocity1[0], velocity2[0]
        
    # Får in x- och y-koordinat när bollen hamnade (cross_position x och y)
    def calculate_accuracy(self, cross_position_x, cross_position_y):
        # error_x och error_y är avståndet från träffpunkten i antalet pixlar
        # Behöver konverteras till cm (kanske?) eller annan längdenhet
       # error_x = self.dodgeball_position_x[-1] - cross_position_x
       # error_y = self.dodgeball_position_y[-1] - cross_position_y
      #  return error_x, error_y
