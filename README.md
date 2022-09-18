# Test 
## Steps to scrape data
1. Scrape web data ethically by setting up user agent.
2. Find out where the data is in the website. In this test, I scraped two websites, I found that in one website, data is stored as a variable in the script, and in the other, data is stored in the html.
3. According to how the data is stored, write code to parse data.
4. Finally, load the data into the database I designed.

## Scraped Webs:
1. http://www.dexel.co.uk/ 
2. https://www.national.co.uk/

## Used input: 205 / 55 / 16

## Methods:
1. BeautifulSoup: good to parse html data.
2. webdriver: good to acquire data in the script.

## Results:
1. database: tyres.db (sqlite) 
2. csv: web1_allTyresData.csv, web2_allTyresData.csv

If you have any questions, please let me know. Thank you!!
