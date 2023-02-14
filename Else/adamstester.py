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
pixle_size_Rare_Wide = float(subPrinted[subPrinted.find("µm")-5: subPrinted.find("µm")])/1000000

rare_camera_wide_stats = [pixles_on_camera_Rare_Wide,camera_aparature_Rare_Wide, short_lens_Rare_Wide,image_sensor_size_Rare_Wide,pixle_size_Rare_Wide]
print(rare_camera_wide_stats)

subPrinted = subPrinted[subPrinted.find("(wide)"):]

pixles_on_camera_Rare_UltraWide = int(subPrinted[subPrinted.find("MP")-3:subPrinted.find("MP")])*1000000
camera_aparature_Rare_UltraWide = subPrinted[(subPrinted.find("MP")+4) : (subPrinted.find("MP"))+10]
short_lens_Rare_UltraWide = int(subPrinted[subPrinted.find("mm")-3: subPrinted.find("mm")])/1000


rare_camera_ultrawide_stats = [pixles_on_camera_Rare_UltraWide,camera_aparature_Rare_UltraWide, short_lens_Rare_UltraWide]
print(rare_camera_ultrawide_stats)

subPrinted = subPrinted[subPrinted.find("(ultrawide)"):]

pixles_on_camera_Rare_Macro = int(subPrinted[subPrinted.find("MP")-2:subPrinted.find("MP")])*1000000
camera_aparature_Rare_Macro = subPrinted[(subPrinted.find("MP")+4) : (subPrinted.find("MP"))+10]
pixle_size_Rare_Macro = float(subPrinted[subPrinted.find("µm")-5: subPrinted.find("µm")-1])/1000000

rare_camera_macro_stats = [pixles_on_camera_Rare_Macro,camera_aparature_Rare_Macro, pixle_size_Rare_Macro]
print(rare_camera_macro_stats)

subPrinted = subPrinted[subPrinted.find("(macro)"):]

pixles_on_camera_Rare_Wide_Pro = int(subPrinted[subPrinted.find("MP")-3:subPrinted.find("MP")])*1000000
camera_aparature_Rare_Wide_Pro = subPrinted[(subPrinted.find("MP")+4) : (subPrinted.find("MP"))+10]
short_lens_Rare_Wide_Pro = int(subPrinted[subPrinted.find("mm")-3: subPrinted.find("mm")])/1000
image_sensor_size_Rare_Wide_Pro = subPrinted[subPrinted.find("mm")+4:subPrinted.find("mm")+10]
pixle_size_Rare_Wide_Pro = float(subPrinted[subPrinted.find("µm")-5: subPrinted.find("µm")])/1000000

rare_camera_wide_stats_Pro = [pixles_on_camera_Rare_Wide_Pro,camera_aparature_Rare_Wide_Pro, short_lens_Rare_Wide_Pro,image_sensor_size_Rare_Wide_Pro,pixle_size_Rare_Wide_Pro]
print(rare_camera_wide_stats_Pro)

subPrinted = subPrinted[subPrinted.find("(ultrawide)"):]

pixles_on_camera_Rare_Telephoto_Pro = int(subPrinted[subPrinted.find("MP")-2:subPrinted.find("MP")])*1000000
camera_aparature_Rare_Telephoto_Pro = subPrinted[(subPrinted.find("MP")+4) : (subPrinted.find("MP"))+10]
pixle_size_Rare_Telephoto_Pro = float(subPrinted[subPrinted.find("µm")-5: subPrinted.find("µm")-1])/1000000

rare_camera_Telephoto_stats_Pro = [pixles_on_camera_Rare_Telephoto_Pro, camera_aparature_Rare_Telephoto_Pro, pixle_size_Rare_Telephoto_Pro]
print(rare_camera_Telephoto_stats_Pro)

subPrinted = subPrinted[subPrinted.find("(telephoto)"):]

pixles_on_camera_Rare_Depth_Pro = int(subPrinted[subPrinted.find("MP")-2:subPrinted.find("MP")])*1000000
camera_aparature_Rare_Depth_Pro = subPrinted[(subPrinted.find("MP")+4) : (subPrinted.find("MP"))+10]

rare_camera_Depth_stats_Pro = [pixles_on_camera_Rare_Depth_Pro, camera_aparature_Rare_Depth_Pro]
print(rare_camera_Depth_stats_Pro)

subPrinted = subPrinted[subPrinted.find("Both"):]

# Kommer börja test-scrapea här.
