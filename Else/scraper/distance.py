from phone_camera import Phone_Camera
from math import sqrt

general_phone_thickness = 8.91/1000
k = 10000000

iPhoneX = Phone_Camera("https://en.wikipedia.org/wiki/IPhone_X")
term1 = (-k*(iPhoneX.apperature) + 2*(iPhoneX.megaPixels)
         * general_phone_thickness)/(4*iPhoneX.megaPixels)
term2 = k*iPhoneX.apperature*general_phone_thickness/iPhoneX.megaPixels
distance = -term1 + sqrt(term2 + term1*term1)
print(distance)

iPhoneXR = Phone_Camera("https://en.wikipedia.org/wiki/IPhone_XR")
term1 = (-k*(iPhoneXR.apperature) + 2*(iPhoneXR.megaPixels)
         * general_phone_thickness)/(4*iPhoneXR.megaPixels)
term2 = k*iPhoneXR.apperature*general_phone_thickness/iPhoneXR.megaPixels
distance = -term1 + sqrt(term2 + term1*term1)
print(distance)
