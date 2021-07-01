import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from random import randrange

main_list = []

# def get_request(url, headers):
#     retries = 5

#     while True:
#         s = time.time()
#         if(retries <= 0):
#             break
#         else:            
#             try:
#                 r = requests.get(url, headers=headers, timeout=10)
#             except: 
#                 # print(err)
#                 # sleep some sec/min and retry here!
#                 sleep_seconds = randrange(5, 20)
#                 time.sleep(sleep_seconds)
#                 retries -= 1
#                 print('Retrying...Retries Left:', retries)
#                 continue
#             else:
#                 is_website_up = r.status_code == 200
#                 return r;

#     if retries <= 0:
#         return "Not Found"

def scrape_for_email(business_page_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.70 Safari/537.36'}

    r = requests.get(business_page_url, headers=headers)

    soup = BeautifulSoup(r.content, 'html.parser')

    try:
        item = soup.find('div', class_ = 'alternateEmailsBlock fontSize4')
        email = item.find('a').text
    except:
        email = ''

    return email


def extract(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.70 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    return soup.find_all('li', class_ = 'listing clearFix')


def transform(articles):
    for item in articles:
        name = item.find('h2', class_ = 'businessName').text

        address = item.find('div', class_ = 'address clearFix').text
        address = address.replace('\n', "")
        address = address.replace('\xa0', " ")

        try:
            # website = item.find('a', class_ = 'btn btn-yellow businessCapsule--ctaItem')['href'] 
            # website = item.find_all('a', attrs={'class': 'btn btn-yellow businessCapsule--ctaItem', 'rel': 'nofollow noopener'})['href']
            website = item.find('a', {'data-yext': 'url'})['href']
        except:
            website = ''

        try:
            tel = item.find('a', class_ = 'phoneCont blue1BG desktopHide')['href']
            tel = tel.replace('tel:', '')
        except:
            tel = ''

        ######################
        info_tab = item.find('li', class_ = 'listingHeadLink blue1BG infoLink')
        business_page = info_tab.find("a")['href']
        # print("business_page:", business_page)

        business_page_url = "https://www.thomsonlocal.com" + business_page

        email = scrape_for_email(business_page_url)
        ######################

        business = {
            'name': name,
            'address': address,
            'website': website,
            'tel': tel,
            'emails': email
        }

        main_list.append(business)
    return


def num_pages(url):
    to_append = '?page=1'
    url = url + to_append

    print('Final URL:', url)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.70 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    pagination_block = soup.find_all('div', class_ = 'paginationBlock clearFix')

    span = ""
    for item in pagination_block:
        span = item.find('span', class_ = 'pageCount').text # 1 - 25 of 99
        if(span):
            break

    lt = span.split("of ")
    items = int(lt[1])

    number = items/25
    number_dec = int(str(number-int(number))[2:])

    if number_dec == 0:
        num_pages = int(number)
    else:
        num_pages = int(number) + 1
        
    return num_pages


def save(file):
    df = pd.DataFrame(main_list)
    df.to_csv(f'{file}.csv', index=False)


def clean_inputs(keyword, location):
    keyword_temp = keyword.lower()
    location_temp = location.lower()
    
    remove_characters = ["& ", "- ", ","]
    for character in remove_characters:
        keyword_temp = keyword_temp.replace(character, "")
    
    keyword_temp = keyword_temp.replace(" ", "-")
    
    location_temp = location_temp.replace(",", "")
    location_temp = location_temp.replace(" ", "-")

    return keyword_temp, location_temp


def run(keyword, location, save_as):
    url = f'https://www.thomsonlocal.com/search/{keyword}/{location}'

    n_pages = num_pages(url)
    print('Number of Pages: ', n_pages)

    for x in range(1, n_pages + 1):
        to_append = '?page={x}'
        cur_url = url + to_append

        print(f'Getting page {x}')

        articles = extract(url)
        transform(articles)

        # randrange gives you an integral value
        sleep_seconds = randrange(5, 20)
        print("Sleep for: " + str(sleep_seconds) + " seconds")
        time.sleep(sleep_seconds)
        print("Continuing..\n")

    save(save_as)
    print('Saved to CSV')


if __name__ == "__main__":

    keyword = 'Car Dealers'
    location = 'London'
    keyword, location = clean_inputs(keyword, location)
    save_as = keyword + "-" + location

    run(keyword, location, save_as)

    print("Number of Businesses Stored (no emails): ", len(main_list))