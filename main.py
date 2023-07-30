from scrape import extract_email, convert_to_csv, extract_prices

test = extract_prices('https://www.pricerunner.dk/deals')
for item in test:
    print(item)