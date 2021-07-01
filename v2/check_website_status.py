import pandas as pd
import re
import requests
import time
from extract_email import *
from extract_email_selenium import *

# import urllib3
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

print(d)

d1 = {}
for (url, value) in d.items():
    if value == True:
        emails_1 = extract_email(url)
        emails_2 = extract_email_selenium(url)

        # print(emails_1)
        # print(type(emails_1))
        # print(emails_2)
        # print(type(emails_2))

        emails = emails_1.union(emails_2)

        emails_str = ", ".join(emails)

        print(emails)

        d1[url] = emails

print(d1)


# df['emails'] = ''

for (url, emails) in d1.items():
    emails = ", ".join(emails)
    # Set emails in df
    df.loc[df['website'] == url, 'emails'] = emails

print(df)
df.to_csv(f'{file}', index=False)