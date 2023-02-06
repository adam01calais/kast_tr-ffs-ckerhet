import numpy as np
from scipy.optimize import curve_fit

class DataAnalysis:
    # Input: bollens poition för kamera 1 och 2
    def __init__(self, positions1, positions2):
        self.positions1 = positions1
        self.positions2 = positions2

    def calculate_velocity(self):
        time = np.linspace(0, len(self.positions1), len(self.positions1))
        velocity1, _ = curve_fit(lambda t, a, b: a*t + b,  time, self.positions1)
        velocity2, _ = curve_fit(lambda t, a, b: a*t + b,  time, self.positions2)
        return velocity1[0], velocity2[0]
        
    def calculate_accuracy(self, cross_position):
        error1 = np.abs(self.positions1[-1] - cross_position)
        error2 = np.abs(self.positions2[-1] - cross_position)
        return error1, error2