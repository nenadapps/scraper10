from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
from time import sleep
from urllib.request import Request
from urllib.request import urlopen

def get_html(url):
    html_content = ''
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()
        html_content = BeautifulSoup(html_page, "html.parser")
    except:
        pass

    return html_content

def get_details(url):

    stamp = {}

    try:
        html = get_html(url)
    except:
        return stamp

    try:
        price = html.select('.pricelarge')[0].get_text()
        price = price.replace(",", "").strip()
        stamp['price'] = price
    except:
        stamp['price'] = None

    try:
        country = html.select("#previewimage h1")[0].get_text()
        stamp['country'] = country
    except:
        stamp['country'] = None

    try:
        sku_temp = html.select('#proddetailscontent p')[0].get_text()
        if 'Ref:' in sku_temp:
            sku = sku_temp.replace('Ref:', '').strip() 
            stamp['sku'] = sku
        else:
            stamp['sku'] = ''
    except:
        stamp['sku'] = None

    try:
        raw_text = html.select('.desc')[0].get_text().strip()
        stamp['raw_text'] = raw_text
    except:
        stamp['raw_text'] = None
        
    try:
        condition = html.select('.prodicons img')[0].get('title').strip()
        stamp['condition'] = condition
    except:
        stamp['condition'] = None    
        

    stamp['currency'] = 'GBP'
    
    # image_urls should be a list
    images = []
    try:
        image_items = html.select('#hero-image img')
        for image_item in image_items:
            img = 'https://www.robinhood-stamp.co.uk' + image_item.get('src')
            images.append(img)
    except:
        pass

    stamp['image_urls'] = images

    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date

    stamp['url'] = url
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 65))
    return stamp

def get_page_items(url):

    items = []
    next_url = ''

    try:
        html = get_html(url)
    except:
        return items, next_url

    try:
        for item in html.select('.prodpanel .imagelinkborder'):
            item = 'https://www.robinhood-stamp.co.uk' + item.get('href')   
            items.append(item)
    except:
        pass

    try:
        next_items = html.select('#pagination a')
        for next_item in next_items:
            next_item_text = next_item.get_text().strip()
            if 'Next' in next_item_text:
                next_url = next_item.get('href')
                break
    except:
        pass

    shuffle(items)

    return items, next_url

def get_countries(url):
    
    items = []

    try:
        html = get_html(url)
    except:
        return items

    try:
        for item in html.select('#content li a'):
            item_href = item.get('href')
            if '_' not in item_href:
                item_link = 'https://www.robinhood-stamp.co.uk' + item_href
                items.append(item_link)
    except:
        pass

    return items

# start url
start_url = 'https://www.robinhood-stamp.co.uk/stock-list'

# loop through all countries
countries = get_countries(start_url)
for country in countries:
    while(country):
        page_items, country = get_page_items(country)
        # loop through all items on current page
        for page_item in page_items:
            stamp = get_details(page_item)
