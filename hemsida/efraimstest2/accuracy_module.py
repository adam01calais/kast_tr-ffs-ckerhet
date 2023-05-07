import numpy as np

def accuracy(x_floor, 
             y_side, 
             ball_radius_side, 
             ball_radius_floor, 
             cross_position_floor_x, 
             cross_position_floor_y, 
             cross_position_side_x, 
             cross_position_side_y, 
             cross_position_floor_x_percentage, 
             cross_position_floor_y_percentage, 
             cross_position_side_x_percentage, 
             cross_position_side_y_percentage,
             video_side_format,  # Add side_format argument
             video_floor_format,
             image_side_format,
             image_floor_format,
             video_side_width,
             video_side_height,
             video_floor_width,
             video_floor_height):
        
        converter_side = 17.78/(2*ball_radius_side)
        converter_floor = 17.78/(2*ball_radius_floor)

        percentage_x = 0
        percentage_y = 0
        cross_coord_x = 0
        cross_coord_y = 0
        video_side_length = 0
        video_floor_length = 0

        # Calculate cross_coord_x and cross_coord_y based on the input formats
        if video_side_format == image_side_format == 'landscape':
                cross_coord_y = cross_position_side_y
                percentage_y = cross_position_side_y_percentage
                video_side_length = video_side_height
        elif video_side_format == image_side_format == 'portrait':
                cross_coord_y = cross_position_side_x
                percentage_y = cross_position_side_x_percentage
                video_side_length = video_side_width
        elif video_side_format == 'landscape' != image_side_format:
                cross_coord_y = cross_position_side_y
                percentage_y = cross_position_side_x_percentage
                video_side_length = video_side_height
        elif video_side_format == 'portrait' != image_side_format:
                cross_coord_y = cross_position_side_x
                percentage_y = cross_position_side_y_percentage
                video_side_length = video_side_width

        if video_floor_format == image_floor_format == 'landscape':
                cross_coord_x = cross_position_floor_x
                percentage_x = cross_position_floor_x_percentage
                video_floor_length = video_floor_width
        elif video_floor_format == image_floor_format == 'portrait':
                cross_coord_x = cross_position_floor_y
                percentage_x = cross_position_floor_y_percentage
                video_floor_length = video_floor_height
        elif video_floor_format == 'landscape' != image_floor_format:
                cross_coord_x = cross_position_floor_x
                percentage_x = cross_position_floor_y_percentage
                video_floor_length = video_floor_width
        elif video_floor_format == 'portrait' != image_floor_format:
                cross_coord_x = cross_position_floor_y
                percentage_x = cross_position_floor_x_percentage
                video_floor_length = video_floor_height

        # Calculate the throw's end position using the percentage values
        cross_coord_x = video_floor_length * percentage_x
        cross_coord_y = video_side_length * percentage_y
        throw_end_position_x = x_floor[-1]
        throw_end_position_y = y_side[-1]

        # Calculate accuracy
        diff_x = -1 * converter_floor * (cross_coord_x - throw_end_position_x)
        diff_y = converter_side * (cross_coord_y - throw_end_position_y)
    
        diff_tot = np.sqrt(diff_x**2 + diff_y**2)
        # print('Bollens avstånd från målet i x-led: ' + str(diff_x) + ' cm')
        # print('Bollens avstånd från målet i y-led: ' + str(diff_y) + ' cm')
        # print('Bollens totala avstånd från målet: ' + str(diff_tot) + ' cm')
        return diff_x, diff_y, round(diff_tot, 1)