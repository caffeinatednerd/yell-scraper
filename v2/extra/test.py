import pandas as pd
import re
# import urllib3
import requests
import time

# http = urllib3.PoolManager()

def working_url(url):
    retries = 5

    while True:
        s = time.time()
        if(retries <= 0):
            break
        else:            
            try:
                r = requests.get(url, timeout=10)
            except: 
                # print(err)
                # sleep some sec/min and retry here!
                time.sleep(10)
                retries -= 1
                print('Retrying...Retries Left:', retries)
                continue
            else:
                is_website_up = r.status_code == 200
                break

    if retries <= 0:
        is_website_up = False
    
    return is_website_up

    # try:
    #     resp = http.request('GET', url)
    # except: 
    #     is_website_up = False
    # else:
    #     is_website_up = resp.status == 200

    # return is_website_up

file = 'Carpenters_Glasgow.csv'

df = pd.read_csv(file)
websites = df["website"]
list_web = websites.unique().tolist()

d = {}
for w in list_web:
    if not pd.isna(w):
        d[w] = None

for w in d:
    # if 'facebook' not in w:
        print('Checking:', w)
        if working_url(w):
            print('Up')
            d[w] = True
        else:
            print('Down')
            d[w] = False

# print(d)

#     extract_email(w)
        #     update_csv()
        # else:
        #     continue