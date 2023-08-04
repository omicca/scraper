from scrape import extract_email, convert_to_csv, extract_prices, convert_to_json

title = extract_prices('https://www.pricerunner.dk/deals')

convert_to_json(title)
