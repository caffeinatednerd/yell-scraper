# Yell.com Scraper

## Targets
1. [x] Scrape Yell.com and save data into CSV (Business Name, Phone No, Address, Website)
2. [x] Check if Website is up and remove duplicate websites before continuing
3. [x] Scrape Email from Landing Page of Website using BeautifulSoup (Not works for emails generated from JS)
4. [x] Scrape Emails from all pages of a Website using Selenium (to counter above problem)
5. [x] Add Thomson Local support
6. [x] Create a Separate Scraper for Facebook business pages
7. [ ] Integrate facebook scraper with extract_all_emails.py
8. [ ] Create a check for finding facebook links with emails when scraping web pages and use the facebook links to find emails
9. [ ] Integrate All Modules

## Misc. Targets
1. [ ] Use Proxy Servers in Python to avoid getting blacklisted
2. [ ] Implement timeout based retry when scraping websites
3. [ ] Create Scraper for other pages mentioned like
4. [ ] Create a tkinter based UI

### Some Other Websites to create Scrapers for 
- Thompsons directory (Easy and Contain Emails + Websites)
- Google 
- Check a trade - Contains no emails (Scraper should Scrape name, website, phone number)
- (Abandoned) Rated people - (Cannot custom search, need to select from available options)
- (Requires Proxy) My builder
