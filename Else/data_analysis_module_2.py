import numpy as np

class DataAnalyzis:

    def __init__(self, x_floor, y_floor, x_side, y_side, frame_rate, ball_radius_floor, ball_radius_side):
        self.frame_rate=frame_rate
        # Här behöver vi konvertera pixlar till cm
        self.converter = 17.78/(ball_radius_floor+ball_radius_side)
        self.x_floor = x_floor
        self.y_floor = y_floor
        self.x_side = x_side
        self.y_side = y_side

    def velocity(self):

        velocity = []
        diff = len(self.x_side) - len(self.y_floor)
        
        del self.x_side[0:diff]
        del self.y_side[0:diff]
        del self.x_side[-1]
        del self.y_floor[-1]
        del self.y_side[-1]
        if self.x_side[0] == 0 or self.y_floor[0] == 0 or self.y_side[0] == 0:
            del self.x_side[0]
            del self.y_floor[0]
            del self.y_side[0]
        for k in range(1,len(self.y_floor)):
            
            if self.x_side[k] == 0: 
                self.x_side[k] = (self.x_side[k-1] + self.x_side[k+1])/2
            if self.y_floor[k] == 0:
                self.y_floor[k] = (self.y_floor[k-1] + self.y_floor[k+1])/2
            if self.y_side[k] == 0:
                self.y_side[k] = (self.y_side[k-1] + self.y_side[k+1])/2
                
            distance_between_frames = np.sqrt((self.x_side[k]-self.x_side[k-1])**2+(self.y_floor[k]-self.y_floor[k-1])**2+(self.y_side[k]-self.y_side[k-1])**2)
            velocity.append(3.6 / 100  * self.converter * distance_between_frames * self.frame_rate)  
        mean_velocity = sum(velocity)/len(velocity)
        print('Hasitgheten för bollen var: ' + str(mean_velocity) + 'km/h')
        return mean_velocity

    def accuracy(self, cross_position_floor_x, cross_position_floor_y, cross_position_side_x, cross_position_side_y):
        # Här behöver vi konvertera pixlar till cm
        cross_coord_x = cross_position_floor_y
        cross_coord_y = cross_position_side_y
        x_coord = self.x_floor[-1]
        y_coord = self.y_side[-1]
        diff_x = cross_coord_x-x_coord
        diff_y = cross_coord_y-y_coord
        diff_tot = self.converter * np.sqrt(diff_x**2 + diff_y**2)
        print('Bollens avstånd från målet: ' + str(diff_tot) + 'cm')
        return diff_x, diff_y, diff_tot