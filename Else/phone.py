from arrays import Phone_Camera

onePlus8 = Phone_Camera("https://en.wikipedia.org/wiki/OnePlus_8")
print(onePlus8.megaPixels)
print(onePlus8.apperature)
print(onePlus8.image_center_size_)
print(onePlus8.pixel_size_)

iPhoneX = Phone_Camera("https://en.wikipedia.org/wiki/IPhone_X")
print(iPhoneX.megaPixels)
print(iPhoneX.apperature)
print(iPhoneX.image_center_size_)
print(iPhoneX.pixel_size_)

#Deapth of field = 2* Focus distance^(2) * apperaure * Confusion/(focal length^(2))
#1/focal length = 1/Focus distance + 1/Phone_thickness
#focal length = Phone_thickness * Focus distance/(Phone_thickness + Focus distance)
#Confusion = focal length^(2)/ (apperature *(Focus distance - focal length))
#Deapth of field = 2* Focus distance^(2) *  apperaure * ((Phone_thickness * Focus distance/(Phone_thickness + Focus distance))^(2)/ (apperature *(Focus distance - (Phone_thickness * Focus distance/(Phone_thickness + Focus distance)))))/((Phone_thickness * Focus distance/(Phone_thickness + Focus distance)^(2)))

