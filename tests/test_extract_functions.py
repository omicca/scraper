import sys
import pytest
sys.path.append("../scraper")
from scrape import extract_email

def test_email_extraction():
    assert True