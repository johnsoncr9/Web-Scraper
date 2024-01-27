Web Scraper for Books to Scrape: README
Overview
This Python script is designed to scrape book data from "Books to Scrape" website. It fetches book titles, prices, ratings, and availability status, writing this information into a CSV file. The script is highly customizable, allowing users to specify the number of pages to scrape and the output file name.

Features
Fetches book details: Title, Price, Rating, and Availability.
Writes data into a CSV file.
Customizable number of pages to scrape.
Customizable output file name.
Error handling for HTTP requests.
Logging of process and errors.
Requirements
Python 3
Libraries: requests, BeautifulSoup (bs4), csv, urllib.parse, logging, time, argparse
Installation
Ensure Python 3 and the required libraries are installed. Use pip to install dependencies if needed:

pip install requests beautifulsoup4
Usage
Run the script from the command line, optionally specifying the output file name and the number of pages to scrape:


python scraper.py --output [output_file.csv] --pages [number_of_pages]
If not specified, the script defaults to data.csv for output and scrapes all pages.

Script Structure
setup_argparse(): Sets up command line arguments for output file and number of pages.
fetch_page(base_url, url): Fetches HTML content from a given URL.
extract_book_data_title(book_element): Extracts book titles.
extract_book_data_prices(book_element): Extracts book prices.
extract_book_data_rating(book_element): Extracts book ratings.
extract_book_data_availability(book_element): Checks book availability.
get_next_page_url(soup): Determines URL for the next page.
parse_html(html_content): Parses HTML content using BeautifulSoup.
Main code block: Orchestrates scraping and writes data to the CSV file.
Logging
Logs are written to scraper.log and printed to the console. It includes timestamps and error messages, aiding in debugging and process tracking.

Limitations
The scraper is specific to the structure of the "Books to Scrape" website. Changes in the website's structure may require script adjustments.
It assumes prices are always in GBP and starts with '£'.
The script is subject to the website's terms of use and scraping ethics.
Disclaimer
Web scraping can be subject to legal and ethical considerations. Ensure compliance with the website's terms of service and applicable laws.





