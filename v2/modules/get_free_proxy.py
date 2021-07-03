import requests
import random
from bs4 import BeautifulSoup as bs
import traceback
import pandas as pd

def get_free_proxies():
    url = "https://free-proxy-list.net/"
    # request and grab content
    soup = bs(requests.get(url).content, 'html.parser')
    # to store proxies
    proxies = []
    for row in soup.find("table", attrs={"id": "proxylisttable"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            proxies.append(str(ip) + ":" + str(port))
        except IndexError:
            continue
    return proxies


def save_working_proxy_list():
    url = "http://httpbin.org/ip"
    proxies = get_free_proxies()
    working_proxies = []

    count = 5

    for i in range(len(proxies)):
        if count == 0:
            break

        #printing req number
        print("Request Number : " + str(i+1))
        proxy = proxies[i]
        try:
            response = requests.get(url, proxies = {"http":proxy, "https":proxy})
            if response.status_code == 200:
                working_proxies.append(proxy)
                count -= 1
            else:
                continue
        except:
            # if the proxy Ip is pre occupied
            continue

    proxies_dict = {'proxy': working_proxies}  
           
    df = pd.DataFrame(proxies_dict) 
        
    # saving the dataframe 
    df.to_csv('C:\\Users\\Prabhu\\Desktop\\yell-scraper\\v2\\proxy\\proxy.csv') 


# save_working_proxy_list()