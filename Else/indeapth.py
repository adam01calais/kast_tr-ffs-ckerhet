from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("https://en.wikipedia.org/wiki/IPhone_X")
bsObj = BeautifulSoup(html.read(), features="html.parser")
printed = str(bsObj.prettify)
subPrinted = printed[printed.find(
    "Rear camera</th>"):printed.find("Connectivity")]
print(subPrinted)
list = []
subPrinted = subPrinted[(subPrinted.find("MP")-5):]
n_pix = subPrinted[0: subPrinted.find("MP")]

while (n_pix[0].isdigit() == False):
    n_pix = n_pix[1:]

list.append(float(n_pix)*1000000)

subPrinted = subPrinted[subPrinted.find("f/")+2:]
apperature = "f/"
while subPrinted[0].isdigit() or subPrinted[0] == ".":
    apperature = apperature + subPrinted[0]
    subPrinted = subPrinted[1:]


list.append(apperature)
print(list)
