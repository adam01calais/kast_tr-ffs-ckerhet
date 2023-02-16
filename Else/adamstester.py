from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("https://en.wikipedia.org/wiki/OnePlus_8")
bsObj = BeautifulSoup(html.read(), features="html.parser")
printed = str(bsObj.prettify)
subPrinted = printed[printed.find(
    "Rear camera</th>"):printed.find("Connectivity")]
subPrinted = subPrinted + "<br/>"



for i in (0,2):
    subPrinted = subPrinted[subPrinted.find("</b>")+4:]
    subPrinted2 = subPrinted[0: subPrinted.find("</b>")]

    while"MP" in subPrinted2:
        pixles_on_camera_Rare = float(
            subPrinted2[0:subPrinted2.find("MP")])*1000000

        subPrinted2 = subPrinted2[subPrinted.find(",")+1:]
        camera_aparature_Rare = "f/" + \
        subPrinted2[(subPrinted2.find("/")+1): (subPrinted2.find(","))]
        subPrinted2 = subPrinted2[subPrinted2.find(",")+1:]
        if "mm" in subPrinted2[0:10]:
            short_lens_Rare = float(subPrinted2[0: subPrinted2.find("mm")])/1000
            subPrinted2 = subPrinted2[subPrinted.find(",")+1:]
        else:
            short_lens_Rare = 0
        if "1/2" in subPrinted2[0:10]:
            image_sensor_size_Rare = subPrinted2[0:subPrinted2.find(",")]
            subPrinted2 = subPrinted2[subPrinted.find(",")+1:]
        else:
            image_sensor_size_Rare = 0
        if "µm" in subPrinted2[0:10]:
            pixle_size_Rare = float(subPrinted2[0: subPrinted2.find("µm")])/1000000
            subPrinted2 = subPrinted2[subPrinted.find(",")+1:]
        else:
            pixle_size_Rare = 0
        rare_camera_stats = [pixles_on_camera_Rare, camera_aparature_Rare,
                         short_lens_Rare, image_sensor_size_Rare, pixle_size_Rare]
        print(rare_camera_stats)
        subPrinted2 = subPrinted2[subPrinted2.find("<br/>")+5:]
        i+=1

