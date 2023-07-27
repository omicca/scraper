from bs4 import BeautifulSoup as soup
import re

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
        email_regex = re.findall("[a-z]+@[a-z]+.[a-z]+", email.string)
        emails += email_regex

    return emails



