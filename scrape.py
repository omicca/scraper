from bs4 import BeautifulSoup as Soup
import re
import requests
import csv
import json
import time
import logging

DOMAIN_URLS = {
    "com": "https://www.pricerunner.com/deals",
    "dk": "https://www.pricerunner.cdk/deals"
}
WATCH_INTERVAL = 60


def extract_email():
    """Extracts emails from HTML file"""
    while True:
        file = input("Enter html filename: ")
        try:
            with open("html/" + file + ".html", "r") as f:
                document = Soup(f, "html.parser")
                break
        except FileNotFoundError:
            print('File not found')
            
    tags = document.find_all('a')

    emails = []
    email_filter = r'(?<=mailto:)\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    for email in tags:
        href = email.get('href', "")
        if href.startswith('mailto:'):
            email_regex = re.findall(email_filter, href, re.DOTALL)
            if email_regex:
                emails += email_regex

    return emails


def extract_prices(url):
    """Extracts name and price of deals from Pricerunner"""
    site_prices = requests.get(url)
    document = Soup(site_prices.text, "html.parser")
    
    final_title = []
    for title in document.find_all('h3', {"class": "pr-1786rw9"}):
        title = title.decode_contents()
        final_title.append(title)

    final_price = []
    for price in document.find_all('span', class_='pr-1859nm3'):
        final_price += price

    final = {}
    i = 0
    for title, price in zip(final_title, final_price):
        final[f'{i}'] = {}
        final[f'{i}']['name'] = title
        final[f'{i}']['price'] = price
        i += 1

    for k, v in final.items():
        if '\xa0' in v['price']:
            v['price'] = v['price'].replace("\xa0", "")

    return final


def price_watcher(domain):
    """Fetches deals every 5 minutes, updating .json
        if new deals or price"""

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(":")
    while True:
        logger.info(f' Watching for .{domain}')
        price_list = {}
        if domain in DOMAIN_URLS:
            url = DOMAIN_URLS[domain]
            price_list = extract_prices(url)

        original_list = convert_to_dict()

        final_list = original_list
        for item_key, item_values in original_list.items():
            original_name = item_values['name']
            for new_item_key, new_item in price_list.items():
                if original_name == new_item['name']:
                    original_price = str(item_values['price'])
                    new_price = new_item['price']
                    original_price = float(original_price.replace("£", ""))
                    new_price = float(new_price.replace("£", ""))

                    if original_price > new_price:
                        logger.info(f"PRICE UPDATE: {original_name} price has changed "
                                    f"from {original_price} to {new_price}")
                        if domain == "com":
                            item_values["price"] = f"{str(new_item['price'])}"
                            convert_to_json(original_list)
                        else:
                            item_values["price"] = f"{str(new_item['price'])}DKK"
                            convert_to_json(original_list)
                else:
                    last_index = int(list(original_list)[-1])
                    last_index += 1

        final_list[f'{last_index}'] = new_item
        convert_to_json(final_list)

        time.sleep(WATCH_INTERVAL)


def convert_to_csv(data_list):
    """Takes list of items and converts to CSV"""
    choice = input("What is being extracted: ")
    with open(f'{choice}_extraction.csv', 'w', newline='') as file:
        email_write = csv.writer(file)
        for item in data_list:
            email_write.writerow([item])


def convert_to_json(data_list):
    """Takes a dictionary or list and converts it to JSON"""
    with open("prices.json", "w") as f:
        json.dump(data_list, f, indent=4, ensure_ascii=False)


def convert_to_dict():
    """Converts a .json file to dictionary"""
    with open("prices.json", "r") as f:
        data = json.load(f)
    return data
