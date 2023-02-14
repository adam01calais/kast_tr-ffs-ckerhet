from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("https://en.wikipedia.org/wiki/OnePlus_8")
bsObj = BeautifulSoup(html.read(), features="html.parser")
printed = str(bsObj.prettify)
subPrinted = printed[printed.find("Rear camera</th>"):printed.find("Connectivity")]


for i in range (0,6):
    pixles_on_camera_Rare= int(subPrinted[subPrinted.find("MP")-2:subPrinted.find("MP")])*1000000
    camera_aparature_Rare = subPrinted[(subPrinted.find("MP")+4) : (subPrinted.find("MP"))+10]
    if "mm" in subPrinted:
        short_lens_Rare = int(subPrinted[subPrinted.find("mm")-3: subPrinted.find("mm")])/1000
        image_sensor_size_Rare = subPrinted[subPrinted.find("mm")+4:subPrinted.find("mm")+7]
        pixle_size_Rare = float(subPrinted[subPrinted.find("µm")-5: subPrinted.find("µm")])/1000000
    

    rare_camera_wide_stats = [pixles_on_camera_Rare,camera_aparature_Rare, short_lens_Rare,image_sensor_size_Rare,pixle_size_Rare]
    print(rare_camera_wide_stats)
    i+=1

    subPrinted = subPrinted[subPrinted.find("<br/>")+3:]


