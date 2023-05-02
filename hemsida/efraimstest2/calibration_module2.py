import cv2
import numpy as np
import os

def calibrate_cross(image1_filename, image2_filename, center1, edge1, center2, edge2, width, height, UPLOAD_FOLDER):
    def get_points(image_path, width, height):
        print(f"Reading image from path: {image_path}")  # Add this line
        img = cv2.imread(image_path)
        img_height, img_width = img.shape[:2]

        if img_width > img_height:  # Landscape image
            new_width = width
            new_height = int(img_height * (width / img_width))
        else:  # Portrait image
            new_height = 2*height
            new_width = 2*int(img_width * (height / img_height))

        img = cv2.resize(img, (new_width, new_height))  # Resize image
        return img

    image1_path = os.path.join(UPLOAD_FOLDER, image1_filename)
    image2_path = os.path.join(UPLOAD_FOLDER, image2_filename)

    img1 = get_points(image1_path, width, height)
    img2 = get_points(image2_path, width, height)


    radius1 = int(np.linalg.norm(np.array(center1) - np.array(edge1)))
    radius2 = int(np.linalg.norm(np.array(center2) - np.array(edge2)))
    cross_position_x1 = center1[0]
    cross_position_y1 = center1[1]
    cross_position_x2 = center2[0]
    cross_position_y2 = center2[1]

    # print('För sidokameran är bollens position: x=' + str(cross_position_x1) + 'y=' + str(cross_position_y1))
    # print('För bottenkameran är bollens position: x=' + str(cross_position_x2) + 'y=' + str(cross_position_y2))
    print('För sidokameran är bollens radie: ' + str(radius1))
    print('För bottenkameran är bollens radie: ' + str(radius2))

    return img1, img2, cross_position_x1, cross_position_y1, cross_position_x2, cross_position_y2, radius1, radius2
