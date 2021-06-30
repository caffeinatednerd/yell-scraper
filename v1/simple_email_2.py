import requests
from bs4 import BeautifulSoup
from email_scraper import scrape_emails
import time

url = 'https://www.qualityjoiners.com/'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.70 Safari/537.36'}
r = requests.get(url, headers=headers)
time.sleep(5)

soup = BeautifulSoup(r.content, 'html.parser')
time.sleep(5)

paragraphs = []
for x in soup:
    paragraphs.append(str(x))

# print(paragraphs)
# print(type(paragraphs[0]))
# print(len(paragraphs))

# for x in paragraphs:
print(scrape_emails(paragraphs[3]))
# print(res)
