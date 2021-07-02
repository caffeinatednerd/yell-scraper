import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from random import randrange
import urllib.parse

import sys
sys.path.append('C:\\Users\\Prabhu\\Desktop\\yell-scraper\\v2\\modules')
from extract_all_emails import extract_all_emails

main_list = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.70 Safari/537.36'}


def extract(url):
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

    # print('Final URL:', url)

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    articles = soup.find_all('div', class_ = 'col-sm-14 col-md-16 col-lg-14 text-center')

    paragraphs = []
    for x in articles:
        paragraphs.append(str(x))

    n_pages = len(paragraphs[0].splitlines()) - 2
    return n_pages

def save(file_name):
    df = pd.DataFrame(main_list)
    file_save_path = "C:\\Users\\Prabhu\\Desktop\\yell-scraper\\v2\\saved_files\\yell.com\\no_emails\\" + file_name
    df.to_csv(file_save_path, index=False)
    print('Saved file at', file_save_path)


def run(keyword, location, save_as):
    url = f'https://www.yell.com/ucs/UcsSearchAction.do?scrambleSeed=55525279&keywords={keyword}&location={location}'

    n_pages = num_pages(url)
    print('Number of Pages: ', n_pages)

    for x in range(1, n_pages + 1):
        to_append = f'&pageNum={x}'
        cur_url = url + to_append

        print(f'Getting page {x}')
        print("Scraping from:", cur_url)

        articles = extract(cur_url)
        transform(articles)
        
        # randrange gives you an integral value
        sleep_seconds = randrange(5, 20)
        print("Sleep for: " + str(sleep_seconds) + " seconds")
        time.sleep(sleep_seconds)
        print("Continuing..\n")

    save(save_as)


def url_string(keyword, location):
    keyword = urllib.parse.quote_plus(keyword)
    location = urllib.parse.quote_plus(location)
    return keyword, location

def get_file_name(keyword, location):
    keyword = keyword.replace(" ", "_")
    location = location.replace(" ", "_")

    return keyword + "-" + location + ".csv"

if __name__ == "__main__":

    platform = 'yell'

    keyword = 'Pizza Delivery & Takeaway'
    location = 'Brighton & Hove City Council'
    file_name = get_file_name(keyword, location)

    keyword, location = url_string(keyword, location)

    run(keyword, location, file_name)

    print("Number of Businesses Stored: ", len(main_list))

    input_file = file_name.replace(".csv", "")
    extract_all_emails(platform, input_file)