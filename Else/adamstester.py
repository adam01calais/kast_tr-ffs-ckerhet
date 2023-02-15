from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("https://en.wikipedia.org/wiki/OnePlus_8")
bsObj = BeautifulSoup(html.read(), features="html.parser")
printed = str(bsObj.prettify)
subPrinted = printed[printed.find(
    "Rear camera</th>"):printed.find("Connectivity")]

subPrinted = subPrinted[subPrinted.find("</b>")+4:]

pixles_on_camera_Rare = float(
    subPrinted[0:subPrinted.find("MP")])*1000000

subPrinted = subPrinted[subPrinted.find(",")+2:]

camera_aparature_Rare = subPrinted[0: (subPrinted.find(" "))]

subPrinted = subPrinted[subPrinted.find(",")+1:]

short_lens_Rare = float(
    subPrinted[0: subPrinted.find("mm")])/1000

subPrinted = subPrinted[subPrinted.find(",")+1:]

image_sensor_size_Rare = subPrinted[0:subPrinted.find(",")]

subPrinted = subPrinted[subPrinted.find(",")+1:]


pixle_size_Rare = float(
    subPrinted[0: subPrinted.find("µm")])/1000000

rare_camera_wide_stats = [pixles_on_camera_Rare, camera_aparature_Rare,
                          short_lens_Rare, image_sensor_size_Rare, pixle_size_Rare]
print(rare_camera_wide_stats)


subPrinted = subPrinted[subPrinted.find("<br/>")+5:]

pixles_on_camera_Rare = float(
    subPrinted[0:subPrinted.find("MP")])*1000000

subPrinted = subPrinted[subPrinted.find(",")+1:]

camera_aparature_Rare = subPrinted[0: (subPrinted.find(","))]

subPrinted = subPrinted[subPrinted.find(",")+1:]

short_lens_Rare = float(
    subPrinted[0: subPrinted.find("mm")])/1000


rare_camera_ultrawide_stats = [pixles_on_camera_Rare,
                               camera_aparature_Rare, short_lens_Rare]
print(rare_camera_ultrawide_stats)

# Kommer börja test-scrapea här.

subPrinted = subPrinted[subPrinted.find("<br/>")+5:]

pixles_on_camera_Rare = float(
    subPrinted[0:subPrinted.find("MP")])*1000000

subPrinted = subPrinted[subPrinted.find(",")+2:]

camera_aparature_Rare = subPrinted[0: (subPrinted.find(" "))]

subPrinted = subPrinted[subPrinted.find(",")+1:]

pixle_size_Rare = float(
    subPrinted[0: subPrinted.find("µm")])/1000000

rare_camera_macro_stats = [pixles_on_camera_Rare,
                           camera_aparature_Rare, pixle_size_Rare]
print(rare_camera_macro_stats)

subPrinted = subPrinted[subPrinted.find("<br/>")+5:]

pixles_on_camera_Rare = float(
    subPrinted[0:subPrinted.find("MP")])*1000000

subPrinted = subPrinted[subPrinted.find(",")+2:]

camera_aparature_Rare = subPrinted[0: (subPrinted.find(" "))]

subPrinted = subPrinted[subPrinted.find(",")+1:]

short_lens_Rare = float(
    subPrinted[0: subPrinted.find("mm")])/1000

subPrinted = subPrinted[subPrinted.find(",")+1:]

image_sensor_size_Rare = subPrinted[0:subPrinted.find(",")]

subPrinted = subPrinted[subPrinted.find(",")+1:]


pixle_size_Rare = float(
    subPrinted[0: subPrinted.find("µm")])/1000000

rare_camera_wide_stats = [pixles_on_camera_Rare, camera_aparature_Rare,
                          short_lens_Rare, image_sensor_size_Rare, pixle_size_Rare]
print(rare_camera_wide_stats)

subPrinted = subPrinted[subPrinted.find("<br/>")+5:]
pixles_on_camera_Rare = float(
    subPrinted[0:subPrinted.find("MP")])*1000000

subPrinted = subPrinted[subPrinted.find(",")+2:]

camera_aparature_Rare = subPrinted[0: (subPrinted.find(" "))]

subPrinted = subPrinted[subPrinted.find(",")+1:]

pixle_size_Rare = float(
    subPrinted[0: subPrinted.find("µm")])/1000000

rare_camera_macro_stats = [pixles_on_camera_Rare,
                           camera_aparature_Rare, pixle_size_Rare]
print(rare_camera_macro_stats)

subPrinted = subPrinted[subPrinted.find("<br/>")+5:]

pixles_on_camera_Rare = float(
    subPrinted[0:subPrinted.find("MP")])*1000000

subPrinted = subPrinted[subPrinted.find(",")+2:]

camera_aparature_Rare = subPrinted[0: (subPrinted.find(" "))]

subPrinted = subPrinted[subPrinted.find(",")+1:]


rare_camera_Depth_stats_Pro = [
    pixles_on_camera_Rare, camera_aparature_Rare]
print(rare_camera_Depth_stats_Pro)

subPrinted = subPrinted[subPrinted.find("Both"):]
