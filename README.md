# scraping_ga_jails
Scraping GA jails for Georgia GOTV Campaign to help to send voter registration and ballot info to every incarcerated person in Georgia's jails. https://ameelio.org/#/

## Contents:

### [henry_county.csv](henry_county.csv)
The output csv file containing all of Henry County, GA's incarcerated persons as of 11/16/20. Contains 3 columns: First (+ Middle) Name, Last Name, Birth Year

### [requirements.txt](requirements.txt)
Contains all of the dependencies for the [spider.py](spider.py) web crawling script.

### [spider.py](spider.py)
Crawler to extract information on Henry County's incarcerated persons found at https://henrycountysheriff.net/Inmate-Search.

## To run:
Navigate to this folder in your terminal. For those unfamiliar with terminal, something like: `cd ~/Downloads/scraping_ga_jails/` will do the trick (assuming you've cloned this repo into Downloads).

### Install dependencies:
Ensure you have `Python 3.7.3` installed. Then enter `pip install -r requirements.txt` to install necessary python packages.

### Execute spider.py script:
Run `python spider.py` to reproduce [henry_county.csv](henry_county.csv). Options include the following:
    * `--help` for help
    * `--num_pages` The number of pages in the database you would like to scrape. Default = 21 because as of 11/16/20 there were 21 pages of incarcerated persons information.
    * `--output_file` The desired name of the output file. By default = 'henry_county_ga.csv'. Note: must end in '.csv'.

## Warning:
For some reason the code didn't want to scrape the very last name on Henry County's website... Couldn't be bothered to sort out why so just added that name manually.