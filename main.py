import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import logging
import time
import argparse

# Setting up logging to write to a file and print to console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("scraper.log"), logging.StreamHandler()],
)

# Start with the initial URL
base_url = "http://books.toscrape.com/catalogue/"
url = "page-1.html"


### Functions
# Setting up argparse
def setup_argparse():
    parser = argparse.ArgumentParser(description="Web Scraper for 'Books to Scrape'")

    parser.add_argument(
        "--output", "-o", type=str, default="data.csv", help="Output CSV file name"
    )
    parser.add_argument(
        "--pages",
        "-p",
        type=int,
        default=None,
        help="Number of pages to scrape, default is all pages",
    )

    return parser.parse_args()


# Fetches a page given a URL.
def fetch_page(base_url, url):
    try:
        response = requests.get(urljoin(base_url, url))
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.text

    except requests.exceptions.RequestException as e:
        logging.error(f"Error during requests to {url}: {str(e)}")
        return None


### Finding book titles
def extract_book_data_title(book_element):
    titles = book_element.find("h3")
    a_tag = titles.find("a")
    return a_tag["title"]
    # logging.info(book_title)


### Finding book prices
def extract_book_data_prices(book_element):
    price_color = book_element.find("p", class_="price_color")
    # Convert price into a float
    price = price_color.text.strip()
    return float(price[2:])  # Assuming price always starts with £
    # logging.info(price)


### Finding book ratings - recording the number of stars as a string.
def extract_book_data_rating(book_element):
    rating_tag = book_element.find("p", class_="star-rating")
    if rating_tag:
        # The class list is something like ['star-rating', 'Three']
        # Take the second class name as the rating
        rating_classes = rating_tag["class"]  # This is a list
        rating = rating_classes[1]  # This should be 'Three', 'One', 'Five', etc.
        # Turn string into int
        ratings_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        rating = ratings_map.get(rating, 0)  # Default to 0 if rating not found
        # logging.info(rating)
    return rating


# Finding availability
def extract_book_data_availability(book_element):
    availability = book_element.find("p", class_="instock availability")
    availability_text = availability.text.strip()  # Removes any extra whitespace
    return "In stock" in availability_text  # Checks if 'In stock' is in the text
    # logging.info(available)  # Will log True if in stock, False otherwise


# URL string of the next page or None if no next page.
def get_next_page_url(soup):
    next_button = soup.find("li", class_="next")
    if next_button:
        return next_button.find("a")["href"]
    else:
        logging.info("Reached last page")
        return None


# Parses the HTML content using BeautifulSoup.
def parse_html(html_content):
    if html_content:
        return BeautifulSoup(html_content, "html.parser")
    else:
        logging.error("No html_content")


### Main Code

# Function to call arg setup
args = setup_argparse()

# Use the output file name specified by the user, or default to 'data.csv'
output_file = args.output

# Open the CSV file for writing
with open(output_file, mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(["Title", "Price-Euro", "Rating", "Availability"])

    # Use the number of pages specified by the user, or scrape all if not specified
    pages_to_scrape = args.pages

    # Flag to count pages for argparse
    page_counter = 0

    # While loop that reads for url = True and pages
    while url and (pages_to_scrape is None or page_counter < pages_to_scrape):
        # Func
        html_content = fetch_page(base_url, url)

        # Func
        soup = parse_html(html_content)

        # For loop to identify all "book" instances
        for book in soup.find_all("article", class_="product_pod"):
            # Func
            data_dict = {}
            book_title = extract_book_data_title(book)
            price = extract_book_data_prices(book)
            rating = extract_book_data_rating(book)
            available = extract_book_data_availability(book)

            # Write the data row for each book
            writer.writerow([book_title, price, rating, available])

        # Add a delay before the next request
        time.sleep(0.001)  # Delay

        # Increment page counter
        page_counter += 1

        # Find link to next page
        url = get_next_page_url(soup)
