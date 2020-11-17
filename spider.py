'''
File: spider.py for crawling https://henrycountysheriff.net/Inmate-Search
Author: Lawrence Chillrud <lgc2139@columbia.edu>
'''
# Package imports:
import selenium as se
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import argparse
#from webdriver_manager.chrome import ChromeDriverManager

# Global variables (can be set from command line).
PAGES = 21
OUTPUT_FILE = 'henry_county.csv'
SHORTEN_MIDDLE_NAME = True

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 25, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def get_args():
    parser = argparse.ArgumentParser(description='Crawls https://henrycountysheriff.net/Inmate-Search for incarcerated voter information.')
    parser.add_argument('--num_pages', type=int, action='store', default=21, help='The number of pages in the database you would like to scrape. Default = 21 because as of 11/16/20 there were 21 pages of incarcerated persons information.')
    parser.add_argument('--output_file', action='store', default='henry_county.csv', help="The desired name of the output file. By default = 'henry_county_ga.csv'. Note: must end in '.csv'.")
    return parser.parse_args()

def setup_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors.
    chrome_options.add_argument("--window-size=1920,1080")
    # driver = webdriver.Chrome(ChromeDriverManager().install()) #for when it's not me using this code...
    driver = se.webdriver.Chrome('/Users/lawrencechillrud/Desktop/chromedriver', options=chrome_options, service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
    return driver

def crawl(driver, url):
    surnames = []
    first_and_middle_names = []
    dobs = []

    driver.get(url)
    search_button = driver.find_element_by_id('dnn_ctr381_ViewInmateSearch_CmdSearch')
    search_button.click()

    # At this point we have page 1 / PAGES up and ready:
    printProgressBar(0, PAGES, prefix='Progress:', suffix='Page 0 / %d complete' % (PAGES))
    for page in range(1, PAGES+3):
        # scrape page:
        data = driver.find_elements_by_tag_name('td')
        record = False
        for i, entry in enumerate(data):
            if not record and entry.text == "View Details":
                record = True

            if record and entry.text == "View Details":
                surnames.append(data[i+1].text)
                first_and_middle_names.append(data[i+2].text + " " + data[i+3].text)
                dobs.append(data[i+4].text)
        if page <= PAGES:
            printProgressBar(page, PAGES, prefix='Progress:', suffix='Page %d / %d complete' % (page, PAGES))
        # change page
        if page != (PAGES + 3):
            try:
                page_button = driver.find_element_by_link_text(str(page+1))
                page_button.click()
            except se.common.exceptions.NoSuchElementException:
                page_button = driver.find_element_by_link_text('...')
                page_button.click()

    
    table = list(zip(first_and_middle_names, surnames, dobs))
    return table

def save_output(scraped_data):
    df = pd.DataFrame.from_records(scraped_data, columns=['First (+ Middle) Name', 'Last Name', 'Birth Year']).sort_values(by='Last Name', ascending=True).reset_index(drop=True)
    df = df.drop_duplicates()
    df.to_csv(OUTPUT_FILE, index=False)

if __name__ == "__main__":
    # Argument parsing:
    args = get_args()
    PAGES = args.num_pages
     
    # Set up chrome driver:
    driver = setup_driver()

    # Crawl!
    scraped_data = crawl(driver, url='https://henrycountysheriff.net/Inmate-Search')
    
    # Output:
    save_output(scraped_data)

