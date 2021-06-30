# from extract_emails.browsers import ChromeBrowser
from extract_emails import EmailExtractor
from extract_emails.browsers import BrowserInterface
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class ChromeBrowser(BrowserInterface):
    def __init__(self):
        # ff_options = Options()
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--headless")
        self._driver = webdriver.Chrome(
            options=options, executable_path="C:\\Users\\Prabhu\\Downloads\\chromedriver.exe",
        )

    def close(self):
        self._driver.quit()

    def get_page_source(self, url: str) -> str:
        self._driver.get(url)
        return self._driver.page_source


def extract_email_selenium(url):    
    with ChromeBrowser() as browser:
        email_extractor = EmailExtractor(url, browser, depth=2)
        emails = email_extractor.get_emails()

    mail_list = []
    for email in emails:
        mail = email.as_list()[0]
        mail_list.append(mail)
        # print(email)
        # print(type(email))
        # print(email.as_dict())
        # print(email.as_list())
        # print(type(email.as_list()))

    print(mail_list)
    return set(mail_list)

# url = 'http://www.kingslandcontracts.co.uk'
# mail_list = extract_email_selenium(url)
# print(mail_list)