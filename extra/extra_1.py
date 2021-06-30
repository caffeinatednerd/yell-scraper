import requests
from lxml import html
import requests.packages.urllib3.exceptions
import json
from urllib3.exceptions import InsecureRequestWarning

# below code send http get request to yellowpages.com
# return content in form of string
# lib Refernce
# 1 :- request

def getRequest(url):
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
    }
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url, verify=False, headers=headers)
    return response.text

# This method is use to parse data from string
# Return object with data
# lib Refrence
# 1 :- lxml
# 2 : json

def parseData(strHtml):
    parser = html.fromstring(strHtml)
    strJson = parser.xpath('//script[@type="application/ld+json"]')[0]
    jObject = json.loads(strJson.text)

    businessName = jObject["name"]
    url = jObject["@id"]
    url = "https://www.yellowpages.com" + url
    streetName = jObject["address"]["streetAddress"]
    locality = jObject["address"]["addressLocality"]
    state = jObject["address"]["addressRegion"]
    country = jObject["address"]["addressCountry"]
    postalCode = jObject["address"]["postalCode"]
    latitude = jObject["geo"]["latitude"]
    longitude = jObject["geo"]["longitude"]
    phone = jObject["telephone"]
    email = jObject["email"]
    email = email.replace("mailto:", "")
    website = jObject["url"]
    numberOfReviews = jObject["aggregateRating"]["reviewCount"]
    rating = jObject["aggregateRating"]["ratingValue"]

    hours = jObject["openingHours"]
    categories = []
    for cat in parser.xpath('//dd[@class="categories"]/span/a'):
        categories.append(cat.text)

    return {
    'Business Name': businessName,
    'URL': url,
    'Street Name': streetName,
    'Locality': locality,
    'State': state,
    'Country': country,
    'Postal Code': postalCode,
    'Latitude': latitude,
    'Longitude': longitude,
    'Phone': phone,
    'Email': email,
    'Website': website,
    'Categories': categories,
    'Hours': hours,
    'Number Of Review': numberOfReviews,
    'Rating': rating
    }

if __name__ == "__main__":
    print('Scraping Data from yellow Pages')
    url = 'https://www.yell.com/biz/j-b-carpentry-barnstaple-901726109/'
    print('Url :- '+url)
    strHtml = getRequest(url)
    result = parseData(strHtml)
    print(result)