import pandas as pd
import re
import requests
import time

import sys
sys.path.append('C:\\Users\\Prabhu\\Desktop\\yell-scraper\\v2\\modules')

from extract_email_bs4 import *
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

def extract_all_emails(platform, file):
    ########################## FORMAT FILENAMES ##############################

    # Format filenames based on platform
    if platform == "yell":
        input_file = "C:\\Users\\Prabhu\\Desktop\\yell-scraper\\v2\\saved_files\\yell.com\\no_emails\\" + file + ".csv"
        output_file = "C:\\Users\\Prabhu\\Desktop\\yell-scraper\\v2\\saved_files\\yell.com\\with_emails\\" + file + "_emails" + ".csv"

        # For Standalone Run of this file
        # input_file = "..\\saved_files\\yell.com\\no_emails\\" + file + ".csv"
        # output_file = "..\\saved_files\\yell.com\\with_emails\\" + file + "_emails" + ".csv" 
    elif platform == "thomson":
        input_file = "C:\\Users\\Prabhu\\Desktop\\yell-scraper\\v2\\saved_files\\thomsonlocal.com\\no_emails\\" + file + ".csv"
        output_file = "C:\\Users\\Prabhu\\Desktop\\yell-scraper\\v2\\saved_files\\thomsonlocal.com\\with_emails\\" + file + "_emails" + ".csv"

        # For Standalone Run of this file
        # input_file = "..\\saved_files\\thomsonlocal.com\\no_emails\\" + file
        # output_file = "..\\saved_files\\thomsonlocal.com\\with_emails\\" + file + "_emails" + ".csv"
    else:
        raise Exception("Platform not supported yet")

    ########################## FILTER URLs ##############################

    print("Reading", input_file)
    df = pd.read_csv(input_file)

    websites = df["website"]
    # Get unique websites from the list    
    list_web = websites.unique().tolist()

    # Initialise dictionary keys with website urls
    d = {}
    for w in list_web:
        if not pd.isna(w):
            d[w] = None

    # Check if website urls are working and filter
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

    ########################## EXTRACT EMAILS ##############################

    # Extract emails of filtered websites using bs4 and selenium (for js based rendering)
    d1 = {}
    for (url, value) in d.items():
        if value == True:
            # emails_1 = extract_email_bs4(url)
            emails_1 = set()
            
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


    ########################## SAVE ##############################

    # df['emails'] = ''

    # Add emails to the correspomding urls in df and save as CSV
    for (url, emails) in d1.items():
        emails = ", ".join(emails)
        # Set emails in df
        df.loc[df['website'] == url, 'emails'] = emails

    print(df)
    df.to_csv(output_file, index=False)


if __name__ == "__main__":

    platform = "yell"
    file = 'Carpenters_Glasgow'

    extract_all_emails(platform, file)