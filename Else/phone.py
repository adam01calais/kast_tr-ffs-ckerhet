from arrays import Phone_Camera
from math import sqrt

general_phone_thickness = 8.91/1000
k = 100000000


OnePlus8 = Phone_Camera("https://en.wikipedia.org/wiki/OnePlus_8")
term1 = (-k*(OnePlus8.apperature) + 2*(OnePlus8.megaPixels)
         * general_phone_thickness)/(4*OnePlus8.megaPixels)
term2 = k*OnePlus8.apperature*general_phone_thickness/OnePlus8.megaPixels
distance = -term1 + sqrt(term2 + term1*term1)
print(distance)
