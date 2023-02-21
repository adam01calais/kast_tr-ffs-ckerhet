import numpy as np

class DataAnalyzis:

    def __init__(self, x_floor, y_floor, x_side, y_side, frame_rate):
        self.frame_rate=frame_rate
        self.converter = 1
        self.x_floor = x_floor
        self.y_floor = y_floor
        self.x_side = x_side
        self.y_side = y_side

    def velocity(self):
        velocity = []
        for k in range(1,len(self.x_floor)-1):
            distance_between_frames = np.sqrt((self.x_side[k+1]-self.x_side[k])**2+(self.y_floor[k+1]-self.y_floor[k])**2+(self.y_side[k+1]-self.y_side[k])**2)
            time = 1/self.frame_rate
            velocity.append(3.6 * 100 * self.converter * distance_between_frames/time)  
        mean_velocity = sum(velocity)/len(velocity)
        print('Hasitgheten för bollen var: ' + str(mean_velocity) + 'km/h')
        return mean_velocity




    def accuracy(self, cross_position_floor_x, cross_position_floor_y, cross_position_side_x, cross_position_side_y):
        # Här behöver vi konvertera pixlar till cm
        cross_coord_x = cross_position_floor_y
        cross_coord_y = cross_position_side_y
        x_coord = self.y_floor[-1]
        y_coord = self.y_side[-1]
        diff_x = cross_coord_x-x_coord
        diff_y = cross_coord_y-y_coord
        diff_tot = np.sqrt(diff_x**2 + diff_y**2)

