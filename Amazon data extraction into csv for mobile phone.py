''' Web extraction using NLP, Selenium, from amazon product search and data
    extraction into a CSV file '''

# Importing necessary libraries
import csv
from bs4 import BeautifulSoup
from selenium import webdriver

# we activate the webdriver for Chrome to extract by using Chrome
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

# Using webdriver we'll now open the Amazon website
url = 'https://www.amazon.in'

# we'll use the get method to activate and use the url
driver.get(url)

# Now we define a function to use the url and extract the particular item page
def get_url(search_term):
    template = 'https://www.amazon.in/s?k={}&crid=RIL0B9JLOKHZ&ref=nb_sb_noss_1'
    
    # we are replacing every space with '+' to adhere with the pattern
    search_term = search_term.replace(" ","+")
    return template.format(search_term)

# checking that the function is working properly and returning the correct url
get_url('mobile phone')

driver.get(url)

# We try and extract the collection for the item 'say mobile phone'
# taking the page source and trying to extract the html using BS
soup = BeautifulSoup(driver.page_source, 'html.parser')

results = soup.find_all('div', {'data-component-type': 's-search-result'})

len(results)

# Prototyping the results
item = results[0]
item.find('div', 'a-section').text

# tagging the name/description element in the html
atag = item.h2.a

atag.text.strip()
description = atag.text.strip()

# we need to extract the url point of this particular point as such that the refence is significant
atag.get('href')
url = "https://www.amazon.in" + atag.get('href')

# Now we extract the price element
item.find('span', 'a-price-whole').text
price = item.find('span', 'a-price-whole').text

# Now we extract the review rating element
item.i.text

rating = item.i.text

item.find('span', 'a-size-base').text
rating_count = item.find('span', 'a-size-base').text

# Generalize the pattern now
def extract_records(item):
    # description and url extraction
    atag = item.h2.a
    description = atag.text.strip()
    url = "https://www.amazon.in" + atag.get('href')
    
    # price
    price = item.find('span', 'a-price-whole').text
    
    # rating and count
    rating = item.i.text
    rating_count = item.find('span', 'a-size-base').text
    
    result = (description, price, rating, rating_count, url)
    
    return result

# Now we try and apply the above to the url and try to extract
records = [] # assigning an empty list
results = soup.find_all('div', {'data-component-type': 's-search-result'})
    
for item in results:
    records.append(extract_records(item))

# Many a times we can encounter a problem where the description might not be same and 
# the components like price/ rating might be missing for some products
# hence exception should be given for these in the custom function
def extract_records(item):
    # description and url extraction
    atag = item.h2.a
    description = atag.text.strip()
    url = "https://www.amazon.in" + atag.get('href')
    
    try:
        # price
        price = item.find('span', 'a-price-whole').text
    except AttributeError:
        price = ''
    
    try:    
        # rating and count
        rating = item.i.text
        rating_count = item.find('span', 'a-size-base').text
    except AttributeError:
        rating = ''
        rating_count = ''
    
    result = (description, price, rating, rating_count, url)
    return result

records = [] # assigning an empty list
results = soup.find_all('div', {'data-component-type': 's-search-result'})
    
for item in results:
    records.append(extract_records(item))

for row in records:
    print(row[1])

''' Now since we have defined the products extraction function with features
    we need to define a function to go to next page, in order to give a range
    of pages to extract the data from'''

def get_url(search_term):
    template = 'https://www.amazon.in/s?k={}&crid=RIL0B9JLOKHZ&ref=nb_sb_noss_1'
    
    # we are replacing every space with '+' to adhere with the pattern
    search_term = search_term.replace(" ","+")
    
    url = template.format(search_term)
    
    url += '&page{}'
    return url

# As we have all the elements in order we need to add all in one place for the extraction to take place properly
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def get_url(search_term):
    template = 'https://www.amazon.in/s?k={}&crid=RIL0B9JLOKHZ&ref=nb_sb_noss_1'
    
    # we are replacing every space with '+' to adhere with the pattern
    search_term = search_term.replace(" ","+")
    
    url = template.format(search_term)
    
    url += '&page{}'
    return url

def extract_records(item):
    # description and url extraction
    atag = item.h2.a
    description = atag.text.strip()
    url = "https://www.amazon.in" + atag.get('href')
    
    try:
        # price
        price = item.find('span', 'a-price-whole').text
    except AttributeError:
        price = ''
    
    try:    
        # rating and count
        rating = item.i.text
        rating_count = item.find('span', 'a-size-base').text
    except AttributeError:
        rating = ''
        rating_count = ''
    
    result = (description, price, rating, rating_count, url)
    return result

def main(search_term):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    record = []
    url = get_url(search_term)
    
    for page in range(1, 21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        for item in results:
            record = extract_records(item)
            if record:
                records.append(record)
    driver.close()
    
    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow({'Description', 'Price', 'Rating', 'Rating_count', 'URL'})
        writer.writerows(records)
        
# Invoking the main function for a keyword
main('mobile phone')






















































