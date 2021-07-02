# import sys
# sys.path.append('C:\\Users\\Prabhu\\Desktop\\yell-scraper\\v2\\modules')

# from extract_all_emails import  

# platform = "yell"
# file = "Carpenters_Glasgow"

# extract_all_emails(platform, file)

import urllib.parse

def clean_inputs(keyword, location):
    keyword = urllib.parse.quote_plus(keyword)
    location = urllib.parse.quote_plus(location)
    return keyword, location

keyword = "Big Mamma's Pizza delivery & Takeaway"
location = "Brighton & Hove City council"

print(clean_inputs(keyword, location))