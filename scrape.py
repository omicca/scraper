from bs4 import BeautifulSoup as soup
import re
import requests
import csv


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
    for email in tags:
        href = email.get('href', "")
        if href.startswith('mailto:'):
            email_regex = re.findall(r'(?<=mailto:)\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', href, re.DOTALL)
            if email_regex:
                emails += email_regex

    return emails

def extract_prices(url):
    """Extracts recent prices from"""
    site_prices = requests.get(url)
    document = soup(site_prices.text, "html.parser")
    
    final_title = []
    for titl in document.find_all('h3', {"class": "pr-1786rw9"}):
        title = titl.parent
        final_title += title.find('h3')

    final_price = []
    for pric in document.find_all('span', class_='pr-1859nm3'):
        final_price += pric

    return final_title, final_price


def convert_to_csv(data_list):
    """Takes list of items and converts to CSV"""
    choice = input("What is being extracted: ")
    with open (f'{choice}_extraction.csv', 'w', newline='') as file:
        email_write = csv.writer(file)
        for item in data_list:
            email_write.writerow([item])
    