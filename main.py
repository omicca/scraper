from scrape import *

price_list = extract_prices("https://www.pricerunner.com/deals")

convert_to_json(price_list)
price_watcher("com")