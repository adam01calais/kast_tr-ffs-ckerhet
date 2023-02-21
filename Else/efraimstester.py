import numpy as np

class DataAnalyzis:

    def __init__(self, x_floor, y_floor, x_side, y_side, frame_rate_floor, frame_rate_side):
        self.frame_rate_floor=frame_rate_floor
        self.frame_rate_side = frame_rate_side
        self.x_floor = x_floor
        self.y_floor = y_floor
        self.x_side = x_side
        self.y_side = y_side

    def velocity(self):
        


    def accuracy(self, cross_position_floor_x, cross_position_floor_y, cross_position_side_x, cross_position_side_y):
        # Här behöver vi konvertera pixlar till cm
        converter = 1
        cross_coord_x = cross_position_floor_y
        cross_coord_y = cross_position_side_y
        x_coord = self.y_floor[-1]
        y_coord = self.y_side[-1]
        diff_x = cross_coord_x-x_coord
        diff_y = cross_coord_y-y_coord
        diff_tot = np.sqrt(diff_x**2 + diff_y**2)

