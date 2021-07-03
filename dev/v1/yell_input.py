import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

main_list = []

def num_pages(url):
    to_append = '&pageNum=1'
    url = url + to_append

    print('Final URL:', url)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.70 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    articles = soup.find_all('div', class_ = 'col-sm-14 col-md-16 col-lg-14 text-center')

    paragraphs = []
    for x in articles:
        paragraphs.append(str(x))

    n_pages = len(paragraphs[0].splitlines()) - 2
    return n_pages


n_pages = num_pages('https://www.yell.com/ucs/UcsSearchAction.do?scrambleSeed=1511728096&keywords=Carpenter&location=Glasgow')
print('Number of Pages: ', n_pages)

