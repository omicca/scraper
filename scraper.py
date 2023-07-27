from bs4 import BeautifulSoup as soup
import re

with open("example.html", "r") as f:
    document = soup(f, "html.parser")

tags = document.find_all('a')

emails = []
for email in tags:
    email_regex = re.findall("[a-z]+@[a-z]+.[a-z]+", email.string)
    emails += email_regex


print(emails)
