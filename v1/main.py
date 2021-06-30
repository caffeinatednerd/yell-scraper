import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

main_list = []

def extract(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.70 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    return soup.find_all('div', class_ = 'row businessCapsule--mainRow')

def transform(articles):
    for item in articles:
        name = item.find('h2', class_ = 'businessCapsule--name text-h2').text
        address = item.find('span', {'itemprop': 'address'}).text.strip().replace('\n', '')
        try:
            website = item.find('a', class_ = 'btn btn-yellow businessCapsule--ctaItem')['href'] 
            # website = item.find_all('a', attrs={'class': 'btn btn-yellow businessCapsule--ctaItem', 'rel': 'nofollow noopener'})['href']
            # website = item.find('a', attrs={'data-tracking': lambda e: e.endswith('WL:CLOSED') if e else False})['href']
        except:
            website = ''
        try:
            tel = item.find('span', class_ = 'business--telephoneNumber').text
        except:
            tel = ''

        business = {
            'name': name,
            'address': address,
            'website': website,
            'tel': tel
        }

        main_list.append(business)
    return

def save_as(file):
    df = pd.DataFrame(main_list)
    df.to_csv(f'{file}.csv', index=False)

url = 'https://www.yell.com/ucs/UcsSearchAction.do?scrambleSeed=7&keywords={keywords}&location={location}&pageNum=1'

for x in range(1, 11):
    print(f'Getting page {x}')
    articles = extract(f'https://www.yell.com/ucs/UcsSearchAction.do?keywords=Cafes+%26+Coffee+Shops&location=Glasgow&scrambleSeed=1282493474&pageNum={x}')
    transform(articles)
    time.sleep(5)

save('')
print('Saved to CSV')