import numpy as np

def velocity(x_side, y_side, x_floor, y_floor, ball_radius_side, ball_radius_floor, frame_rate):

        # Skapar en lista för hastigheten
        velocity = []

        converter_side = 17.78/(2*ball_radius_side)
        converter_floor = 17.78/(2*ball_radius_floor)
        
        # Tar bort alla värden för bilder då en boll ej var detekterad, 
        # fram tills första detekterade bollen
        for element in x_floor[:]:
            if int(element) == 0:
                x_floor.remove(element) 
            else:
                break
        for element in y_floor[:]:
            if int(element) == 0:
                y_floor.remove(element) 
            else:
                break
        for element in x_side[:]:
            if int(element) == 0:
                x_side.remove(element) 
            else:
                break
        for element in y_side[:]:
            if int(element) == 0:
                y_side.remove(element)
            else:
                break

        count = 0
        for element in range(0, len(x_floor)):
            if x_floor[element] == 0:
                count += 1
                continue
            if count == 1:
                x_floor[element-count] = x_floor[element-count-1] - (x_floor[element-count-1] - x_floor[element])/(count+1)
                count = 0
            elif count == 2:
                x_floor[element-count] = x_floor[element-count-1] - (x_floor[element-count-1] - x_floor[element])/(count+1)
                x_floor[element-count+1] = x_floor[element-count] - (x_floor[element-count-1] - x_floor[element])/(count+1)
                count = 0
            elif count > 2:
                print('Kastet kunde ej detekterades väl nog')
        count = 0
        for element in range(0, len(y_floor)):
            if y_floor[element] == 0:
                count += 1
                continue
            if count == 1:
                y_floor[element-count] = y_floor[element-count-1] - (y_floor[element-count-1] - y_floor[element])/(count+1)
                count = 0
            elif count == 2:
                y_floor[element-count] = y_floor[element-count-1] - (y_floor[element-count-1] - y_floor[element])/(count+1)
                y_floor[element-count+1] = y_floor[element-count] - (y_floor[element-count-1] - y_floor[element])/(count+1)
                count = 0
            elif count > 2:
                print('Kastet kunde ej detekterades väl nog')
        count = 0
        for element in range(0, len(x_side)):
            if x_side[element] == 0:
                count += 1
                continue
            if count == 1:
                x_side[element-count] = x_side[element-count-1] + (x_side[element] - x_side[element-count-1])/(count+1)
                count = 0
            elif count == 2:
                x_side[element-count] = x_side[element-count-1] + (x_side[element] - x_side[element-count-1])/(count+1)
                x_side[element-count+1] = x_side[element-count] + (x_side[element] - x_side[element-count-1])/(count+1)
                count = 0
            elif count > 2:
                print('Kastet kunde ej detekterades väl nog')
        count = 0
        for element in range(0, len(y_side)):
            if y_side[element] == 0:
                count += 1
                continue
            if count == 1:
                y_side[element-count] = y_side[element-count-1] - (y_side[element-count-1] - y_side[element])/(count+1)
                count = 0
            elif count == 2:
                y_side[element-count] = y_side[element-count-1] - (y_side[element-count-1] - y_side[element])/(count+1)
                y_side[element-count+1] = y_side[element-count] - (y_side[element-count-1] - y_side[element])/(count+1)
                count = 0
            elif count > 2:
                print('Kastet kunde ej detekterades väl nog')

        diff = len(x_side) - len(y_floor)

        if diff < 0:
            del x_floor[0:-diff]
            del y_floor[0:-diff]
            del x_floor[-2:]
            del y_floor[-2:]
            del x_side[-2:]
            del y_side[-2:]
        elif diff > 0:
            del x_side[0:diff]
            del y_side[0:diff]
            del x_floor[-2:]
            del y_floor[-2:]
            del x_side[-2:]
            del y_side[-2:]
        
        for k in range(1,len(y_floor)):     
            distance_between_frames = np.sqrt((converter_side*(x_side[k]-x_side[k-1]))**2+(converter_floor*(y_floor[k]-y_floor[k-1]))**2+(converter_side*(y_side[k]-y_side[k-1]))**2)
            velocity.append(3.6 / 100 * distance_between_frames * frame_rate)  
        mean_velocity = sum(velocity)/len(velocity)
        print('Hasitgheten för bollen var: ' + str(mean_velocity) + ' km/h')
        return round(mean_velocity, 1)