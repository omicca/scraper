import sys
import pytest
sys.path.append("../scraper")
import scrape as sc

def test_email_extraction_to_csv(monkeypatch):
    """Test that checks if the function extract_email()
        extracts emails correctly from HTML document"""
    monkeypatch.setattr('builtins.input', lambda _: "html_tests")

    expected_output = ["email1@example.com", "email2@example.com", "email3@example.com", 
                       "email4@example.com", "email5@example.com", "email100@example.com"]

    result = sc.extract_email()
    assert result == expected_output