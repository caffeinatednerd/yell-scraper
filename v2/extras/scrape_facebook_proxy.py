from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

import sys
sys.path.append('C:\\Users\\Prabhu\\Desktop\\yell-scraper\\v2\\modules')
from get_free_proxy import save_working_proxy_list

usr = 'roc8hq@gmail.com'
pwd = 'maitanayhoon'

def scrape_facebook_emails(url_to_scrape, use_proxy=False):
    url = "https://www.facebook.com/login"

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    prefs = {
      "translate_whitelists": {"hi":"en"},
      "translate":{"enabled":"true"}
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--headless")

    if use_proxy == True:
        save_working_proxy_list()
        df = pd.read_csv('C:\\Users\\Prabhu\\Desktop\\yell-scraper\\v2\\proxy\\proxy.csv')
        proxies = df['proxy'].tolist()

        for PROXY in proxies:
            try:
                options.add_argument('--proxy-server=%s' % PROXY)
                
                driver = webdriver.Chrome(options=options, executable_path='C:\\Users\\Prabhu\\Desktop\\yell-scraper\\v2\\dependencies\\chromedriver.exe')
                driver.get(url)

                username_box = driver.find_element_by_id('email')
                username_box.send_keys(usr)
                print ("Email Id entered")
                sleep(1)
                  
                password_box = driver.find_element_by_id('pass')
                password_box.send_keys(pwd)
                print ("Password entered")
                  
                login_box = driver.find_element_by_id('loginbutton')
                login_box.click()
                  
                print ("Logged In")

                wait = WebDriverWait(driver, 30)
                # wait.until(EC.url_changes('https://www.facebook.com/?sk=welcome'))
                # driver.get('https://www.facebook.com/home.php')
                wait.until(EC.url_changes('https://www.facebook.com/home.php'))

                sleep(10)

                try:
                    driver.get(url_to_scrape)
                    driver.implicitly_wait(10)
                # wait.until(EC.url_changes('https://www.facebook.com/JSS-joiners-2334784586744760'))

                # try:
                #     el = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl py34i1dx gpro0wi8']")))
                #     WebDriverWait(driver, 10).until(lambda d: 'gpro0wi8' not in el.get_attribute('class'))
                # finally:
                #     driver.quit()


                # print(el)

                # elements = driver.find_elements_by_class_name("oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl py34i1dx gpro0wi8")
                # elements = driver.find_element_by_css_selector('a.oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl py34i1dx gpro0wi8')
                    elements = driver.find_elements_by_partial_link_text("@")
                    driver.quit()
                except:
                    continue

                for link in elements:
                    emails = link.get_attribute("href")

                return emails
                # break
            except:
                continue
    

url_to_scrape = "https://www.facebook.com/Aye-Light-Electrical-1542154799400655"
emails = scrape_facebook_emails(url_to_scrape, True)
print(emails)