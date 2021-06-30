from extract_emails import EmailExtractor
from extract_emails.browsers import ChromeBrowser
from selenium import webdriver

# webdriver = new ChromeDriver();

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=options, executable_path='C:\\Users\\Prabhu\\Downloads\\chromedriver.exe')

print(type(browser))

browser.get("http://www.google.com")
myPageTitle = browser.title
print(myPageTitle)
print(browser.quit)
browser.quit

# email_extractor = EmailExtractor("http://www.tomatinos.com/", browser, depth=2)
# emails = email_extractor.get_emails()

# for email in emails:
#     print(email)
#     print(email.as_dict())