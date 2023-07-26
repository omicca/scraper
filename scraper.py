from bs4 import BeautifulSoup

with open("example.html", "r") as f:
    document = BeautifulSoup(f, "html.parser")
    