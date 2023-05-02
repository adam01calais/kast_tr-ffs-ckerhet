from phone_camera import Phone_Camera
from math import sqrt
from scipy.special import lambertw
from math import tan

<<<<<<< HEAD
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
=======
OnePlus8 = Phone_Camera("https://en.wikipedia.org/wiki/OnePlus_8")
<<<<<<< HEAD
i= 0.0357143*lambertw(16.0604*sqrt(OnePlus8.megaPixels))
o = i*tan(1)/(0.000000560*OnePlus8.apperature*i-tan(1))

print(OnePlus8.apperature)
print(OnePlus8.megaPixels)
print(abs(o.real))
=======
print(OnePlus8.general_distance)
>>>>>>> a7fc2bd10f82ee998b79c2c4072b86211158164a
>>>>>>> bd7cba92deea4a25eb7786ebddc4fab83ff5edf0
