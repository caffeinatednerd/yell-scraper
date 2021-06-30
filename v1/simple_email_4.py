from bs4 import BeautifulSoup
import urllib3
import re
import requests

http = urllib3.PoolManager()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.70 Safari/537.36'}
url = 'https://www.procraftjoinery.co.uk/'
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')

paragraphs = []
for x in soup:
    paragraphs.append(str(x))

pattern = "[\w\d_.]+@[\w\d_]+.[\w\d_.]+"

for i in paragraphs:
    redata = re.findall(pattern, i)
    for address in redata:
        print(address)