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
            # website = item.find('a', class_ = 'btn btn-yellow businessCapsule--ctaItem')['href'] 
            # website = item.find_all('a', attrs={'class': 'btn btn-yellow businessCapsule--ctaItem', 'rel': 'nofollow noopener'})['href']
            website = item.find('a', attrs={'data-tracking': lambda e: e.endswith('WL:CLOSED') if e else False})['href']
        except:
            website = ''
        try:
            tel = item.find('span', class_ = 'business--telephoneNumber').text
        except:
            tel = ''

        # TODO: Add emails as empty here
        business = {
            'name': name,
            'address': address,
            'website': website,
            'tel': tel
        }

        main_list.append(business)
    return

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

def save(file):
    df = pd.DataFrame(main_list)
    df.to_csv(f'{file}.csv', index=False)


def run(keyword, location, save_as):
    url = f'https://www.yell.com/ucs/UcsSearchAction.do?scrambleSeed=7&keywords={keyword}&location={location}'

    n_pages = num_pages(url)
    print('Number of Pages: ', n_pages)

    for x in range(1, n_pages):
        to_append = '&pageNum={x}'
        cur_url = url + to_append

        print(f'Getting page {x}')

        articles = extract(url)
        transform(articles)
        time.sleep(5)

    save(save_as)
    print('Saved to CSV')


if __name__ == "__main__":

    keyword = 'Carpenter'
    location = 'Glasgow'
    save_as = 'Carpenters_Glasgow'

    run(keyword, location, save_as)