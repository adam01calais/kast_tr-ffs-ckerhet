from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("https://en.wikipedia.org/wiki/OnePlus_8")
bsObj = BeautifulSoup(html.read(), features="html.parser")
printed = str(bsObj.prettify)
subPrinted = printed[printed.find("Rear camera</th>"):printed.find("Connectivity")]

# Kommer börja test-scrapea här.
