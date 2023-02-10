from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("https://www.walmart.com/ip/Used-OnePlus-8-5G-GSM-Unlocked-128GB-Interstellar-Glow-Black/589716447")
bsObj = BeautifulSoup(html.read())
print(bsObj.prettify)
# Kommer börja test-scrapea här. 
