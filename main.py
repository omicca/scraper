from scrape import extract_email, convert_to_csv

emails = extract_email()

print(emails)

convert_to_csv(emails)