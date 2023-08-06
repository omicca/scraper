from bs4 import BeautifulSoup as soup
import re
import requests
import csv
import json


def extract_email():
    """Extracts emails from HTML file"""
    while True:
        file = input("Enter html filename: ")
        try:
            with open("html/" + file + ".html", "r") as f:
                document = soup(f, "html.parser")
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
    """Extracts prices of deals from pricerunner"""
    site_prices = requests.get(url)
    document = soup(site_prices.text, "html.parser")
    
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


def convert_to_csv(data_list):
    """Takes list of items and converts to CSV"""
    choice = input("What is being extracted: ")
    with open (f'{choice}_extraction.csv', 'w', newline='') as file:
        email_write = csv.writer(file)
        for item in data_list:
            email_write.writerow([item])

def convert_to_json(data_list):
    """Takes a dictionary and converts it to JSON"""
    with open("prices.json", "w") as f:
        json.dump(data_list, f, indent=4, ensure_ascii=False)
