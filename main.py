from scrape import *

test = extract_prices("https://www.pricerunner.com/deals")
convert_to_json(test)
prices = price_watcher("com")
