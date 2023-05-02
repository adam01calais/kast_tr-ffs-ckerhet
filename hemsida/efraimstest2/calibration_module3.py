import cv2
import numpy as np
import os

def get_image_format(img):
    img_height, img_width = img.shape[:2]
    if img_width > img_height:
        return 'landscape'
    else:
        return 'portrait'

def rotate_to_landscape(img):
    img_height, img_width = img.shape[:2]
    if img_width < img_height:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    return img

def resize_image(img, width, height):
    img_height, img_width = img.shape[:2]
    
    new_width = width
    new_height = int(img_height * (width / img_width))
    
    scaling_factors = (img_width / new_width, img_height / new_height)
    resized_img = cv2.resize(img, (new_width, new_height))
    
    return resized_img, scaling_factors

def adjust_points(points, scaling_factors):
    return [point * scaling for point, scaling in zip(points, scaling_factors)]

def calibrate_cross(image1_filename, image2_filename, center1, edge1, center2, edge2, width1, height1, width2, height2, orig_width1, orig_height1, orig_width2, orig_height2, UPLOAD_FOLDER):
    image1_path = os.path.join(UPLOAD_FOLDER, image1_filename)
    image2_path = os.path.join(UPLOAD_FOLDER, image2_filename)

    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)

    image1_format = get_image_format(img1)
    image2_format = get_image_format(img2)

    scaling_factors1 = (orig_width1 / width1, orig_height1 / height1)
    scaling_factors2 = (orig_width2 / width2, orig_height2 / height2)

    img1, _ = resize_image(img1, width1, height1)
    img2, _ = resize_image(img2, width2, height2)

    adjusted_center1 = adjust_points(center1, scaling_factors1)
    adjusted_edge1 = adjust_points(edge1, scaling_factors1)
    adjusted_center2 = adjust_points(center2, scaling_factors2)
    adjusted_edge2 = adjust_points(edge2, scaling_factors2)

    radius1 = int(np.linalg.norm(np.array(adjusted_center1) - np.array(adjusted_edge1)))
    radius2 = int(np.linalg.norm(np.array(adjusted_center2) - np.array(adjusted_edge2)))

    cross_position_x1, cross_position_y1 = adjusted_center1
    cross_position_x2, cross_position_y2 = adjusted_center2

    cross_position_x1_percentage = cross_position_x1 / orig_width1
    cross_position_y1_percentage = cross_position_y1 / orig_height1
    cross_position_x2_percentage = cross_position_x2 / orig_width2
    cross_position_y2_percentage = cross_position_y2 / orig_height2

    # print(f'För sidokameran är bollens radie: {radius1}')
    # print(f'För bottenkameran är bollens radie: {radius2}')

    return img1, img2, cross_position_x1, cross_position_y1, cross_position_x2, cross_position_y2, radius1, radius2, cross_position_x1_percentage, cross_position_y1_percentage, cross_position_x2_percentage, cross_position_y2_percentage, image1_format, image2_format
