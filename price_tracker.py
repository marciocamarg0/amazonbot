import requests
from bs4 import BeautifulSoup
import time

# Function to fetch and parse price from a webpage
def fetch_price(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx, 5xx)

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Locate the price based on the provided HTML structure
        price_whole = soup.find('span', class_='a-price-whole')
        price_fraction = soup.find('span', class_='a-price-fraction')
        
        if price_whole and price_fraction:
            # Combine whole and fraction parts
            price = price_whole.text + '.' + price_fraction.text
            currency = soup.find('span', class_='a-price-symbol').text.strip()
            return price, currency
        else:
            return None, None
    except Exception as e:
        print(f"Error fetching price for {url}: {e}")
        return None, None

# Function to check prices for a list of URLs
def check_prices(url_file):
    # Read URLs from the provided text file
    with open(url_file, 'r') as file:
        urls = file.readlines()

    # Strip any leading/trailing whitespace characters
    urls = [url.strip() for url in urls]

    # Store previous prices to detect changes
    previous_prices = {}

    while True:
        for url in urls:
            print(f"Checking price for: {url}")
            price, currency = fetch_price(url)

            if price:
                print(f"Current price for {url}: {currency} {price}")
                # Check if price has changed since the last check
                if url in previous_prices:
                    if previous_prices[url] != price:
                        print(f"Price has changed for {url}: {previous_prices[url]} -> {price}")
                previous_prices[url] = price
            else:
                print(f"Could not fetch price for {url}")

        print("Checking prices again in 2 minutes...")
        time.sleep(120)  # Sleep for 2 minutes before checking again

# Run the price checker on a text file containing URLs
if __name__ == "__main__":
    check_prices("product_urls.txt")  # Replace with your file name containing URLs
