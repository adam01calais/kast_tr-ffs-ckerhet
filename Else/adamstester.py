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
pixle_size_Rare_Wide = int(subPrinted[subPrinted.find("µm")-2: subPrinted.find("µm")])*0.0000001

rare_camera_wide_stats = [pixles_on_camera_Rare_Wide,camera_aparature_Rare_Wide, short_lens_Rare_Wide,image_sensor_size_Rare_Wide,pixle_size_Rare_Wide]
print(rare_camera_wide_stats)

subPrinted = subPrinted[subPrinted.find("(wide)"):]

pixles_on_camera_Rare_UltraWide = int(subPrinted[subPrinted.find("MP")-3:subPrinted.find("MP")])*1000000
camera_aparature_Rare_UltraWide = subPrinted[(subPrinted.find("MP")+4) : (subPrinted.find("MP"))+10]
short_lens_Rare_UltraWide = int(subPrinted[subPrinted.find("mm")-3: subPrinted.find("mm")])/1000
image_sensor_size_Rare_UltraWide = subPrinted[subPrinted.find("mm")+4:subPrinted.find("mm")+7]
pixle_size_Rare_UltraWide = int(subPrinted[subPrinted.find("µm")-2: subPrinted.find("µm")])*0.0000001

rare_camera_ultrawide_stats = [pixles_on_camera_Rare_UltraWide,camera_aparature_Rare_UltraWide, short_lens_Rare_UltraWide,image_sensor_size_Rare_UltraWide,pixle_size_Rare_UltraWide]
print(rare_camera_ultrawide_stats)

# Kommer börja test-scrapea här.
