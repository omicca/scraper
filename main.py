from scrape import extract_email, convert_to_csv, extract_prices, convert_to_json

prices = extract_prices('https://www.pricerunner.com/deals')

convert_to_json(prices)