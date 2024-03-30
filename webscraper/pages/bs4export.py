from bs4 import BeautifulSoup
from selenium import webdriver
from format_text import trunc
import os

def scrape_text_from_url(url):
    # Send a GET request to the URL
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    
    # Check if the request was successful
    # Parse the HTML content of the page
    html = driver.page_source

    driver.close()

    soup = BeautifulSoup(html, 'html5lib')
    
    # Find the main_content element
    main_content = soup.find(class_='maincontent')
    block_content_outer = soup.find(class_='block_content_outer')
    content = soup.find(class_='content')
    
    if main_content:
        # Extract text from main_content element
        page_text = main_content.get_text(separator='\n').strip()
        return page_text
    elif block_content_outer:
        page_text = block_content_outer.get_text(separator='\n').strip()
        return page_text
    elif content:
        page_text = content.get_text(separator='\n').strip()
        return page_text
    else:
        print(f"NOT FOUND {url}")
        return None

# Example usage:
def make(title, url):
    # check if txt file already exists
    if os.path.exists(f"webscraper/pages/txts_bs4/{trunc(title)}.txt"):
        print(f"File {trunc(title)}.txt already exists")
        return
    # title = "Computational Science and Engineering Track"
    # url = "https://www.cs.purdue.edu/undergraduate/curriculum/track-cse-fall2023.html"
    scraped_text = scrape_text_from_url(url)
    if scraped_text:
        # get rid of the extra newlines
        scraped_text = '\n'.join([line for line in scraped_text.split('\n') if line.strip()])
        with open(f'webscraper/pages/txts_bs4/{trunc(title)}.txt', 'w') as file:
            file.write(url + '\n')
            file.write(scraped_text)
