# from extract_emails.browsers import ChromeBrowser
# from extract_emails import EmailExtractor, ContactInfoLinkFilter
import extract_emails
from extract_emails.browsers import BrowserInterface
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

class ChromeBrowser(BrowserInterface):
    def __init__(self):
        # ff_options = Options()
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--headless")
        options.add_argument("enable-automation")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--dns-prefetch-disable")
        options.add_argument("--disable-gpu")
        # options.add_argument("enable-features=NetworkServiceInProcess")
        options.add_argument("disable-features=NetworkService")
        options.page_load_strategy = 'eager'

        self._driver = webdriver.Chrome(
            options=options, executable_path="C:\\Users\\Prabhu\\Desktop\\yell-scraper\\v2\\dependencies\\chromedriver.exe",
        )

    def close(self):
        self._driver.quit()

    def get_page_source(self, url: str) -> str:
        self._driver.get(url)
        return self._driver.page_source


def filter_contact_links(url):
    with ChromeBrowser() as browser:
        # email_extractor = EmailExtractor(url, browser, depth=1)
        # ContactInfoLinkFilter.filter(url)
        contact_links = extract_emails.link_filters.ContactInfoLinkFilter.links(url)
        return contact_links

url = ['http://www.qasltd.co.uk']
mail_list = filter_contact_links(url)
print(mail_list)