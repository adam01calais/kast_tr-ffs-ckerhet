from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("https://en.wikipedia.org/wiki/OnePlus_8")
bsObj = BeautifulSoup(html.read(), features="html.parser")
printed = str(bsObj.prettify)
subPrinted = printed[printed.find("Rear camera</th>"):printed.find("Connectivity")]
print(subPrinted)
pixles_on_camera_Rare_Wide = int(subPrinted[subPrinted.find("MP")-3:subPrinted.find("MP")])*1000000
camera_aparature_Rare_Wide = subPrinted[(subPrinted.find("MP")+4) : (subPrinted.find("MP"))+10]
short_lens_Rare_Wide = int(subPrinted[subPrinted.find("mm")-3: subPrinted.find("mm")])/1000
image_sensor_size_Rare_Wide = subPrinted[subPrinted.find("mm")+4:subPrinted.find("mm")+7]

print(pixles_on_camera_Rare_Wide)
print(camera_aparature_Rare_Wide)
print(short_lens_Rare_Wide) 
print(image_sensor_size_Rare_Wide)
# Kommer börja test-scrapea här.
