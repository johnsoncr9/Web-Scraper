###Potential Functions to Create


# fetch_page(url): Fetches a page given a URL.
# Inputs: URL as a string.
# Outputs: The HTML content of the page.
def fetch_page(url):
    try:
        response = requests.get(urljoin(base_url, url))
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.text

    except requests.exceptions.RequestException as e:
        logging.error(f"Error during requests to {url}: {str(e)}")
        return None


# parse_html(html_content): Parses the HTML content using BeautifulSoup.
# Inputs: HTML content as a string.
# Outputs: A BeautifulSoup object.
def parse_html(html_content):
    try html_content:
      return BeautifulSoup(html_content, "html.parser")
    Except:
      logging_error("No html_content")


# extract_book_data(book_element): Extracts data like title, price, rating, and availability from a single book element.
# Inputs: A single book element (BeautifulSoup object).
# Outputs: A dictionary with book details (title, price, rating, available).
def extract_book_data(book_element):
   for book in soup.find_all("article", class_="product_pod"):
      ### Finding book titles
      titles = book.find("h3")
      a_tag = titles.find("a")
      book_title = a_tag["title"]
      # logging.info(book_title)

      ### Finding book prices
      price_color = book.find("p", class_="price_color")
      # Convert price into a float
      price = price_color.text.strip()
      price = float(price[2:])  # Assuming price always starts with £
      # logging.info(price)

      ### Finding book ratings - recording the number of stars as a string.
      rating_tag = book.find("p", class_="star-rating")
      if rating_tag:
          # The class list is something like ['star-rating', 'Three']
          # Take the second class name as the rating
          rating_classes = rating_tag["class"]  # This is a list
          rating = rating_classes[
              1
          ]  # This should be 'Three', 'One', 'Five', etc.
          # Turn string into int
          ratings_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
          rating = ratings_map.get(rating, 0)  # Default to 0 if rating not found
          # logging.info(rating)

      # Finding availability
      availability = book.find("p", class_="instock availability")
      availability_text = (
          availability.text.strip()
      )  # Removes any extra whitespace
      available = (
          "In stock" in availability_text
      )  # Checks if 'In stock' is in the text
      # logging.info(available)  # Will log True if in stock, False otherwise

      # Write the data row for each book
      writer.writerow([book_title, price, rating, available])

      # Add a delay before the next request
      time.sleep(0.001)  # Delay


# convert_price(price_str): Converts a price string to a numerical value.
# Inputs: Price string.
# Outputs: Price as a float.

# convert_rating(rating_str): Converts a rating string to an integer value.
# Inputs: Rating string.
# Outputs: Rating as an integer.

# check_availability(availability_str): Checks if a book is in stock.
# Inputs: Availability string.
# Outputs: Boolean indicating availability.

# write_to_csv(data, filename): Writes given data to a CSV file.
# Inputs: List of dictionaries containing book data, Filename for the CSV.
# Outputs: None (writes to a CSV file).

# get_next_page_url(soup): Finds the URL of the next page.
# Inputs: BeautifulSoup object for the current page.
# Outputs: URL string of the next page or None if no next page.
def get_next_page_url(soup):
   next_button = soup.find("li", class_="next")
   if next_button:
      return next_button.find("a")["href"]
   else:
      logging.info("Reached last page")
      return None

# setup_argparse(): Sets up and parses command-line arguments.
# Inputs: None.
# Outputs: Argparse object with parsed command-line arguments.

def setup_argparse():
    # Creating the parser
    parser = argparse.ArgumentParser(description="Web Scraper for 'Books to Scrape'") 
    # Add arguments
    parser.add_argument(
        "--output", "-o", type=str, default="data.csv", help="Output CSV file name"
    )
    parser.add_argument("--pages", "-p", type=int, help="Number of pages to scrape")  
    # Parse the arguments
    args = parser.parse_args()  
    # Use the arguments in your script
    output_file = args.output
    pages_to_scrape = args.pages