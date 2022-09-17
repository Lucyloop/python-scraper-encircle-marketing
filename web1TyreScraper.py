#
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import sqlite3
import pandas as pd

#set example
width = 205
profile = 55
rim = 16
#web example
scraped_web = 'http://www.dexel.co.uk/'
url = f"http://www.dexel.co.uk/shopping/tyre-results?width={width}&profile={profile}&rim={rim}&speed=."

"""
'Please note that you must attempt to be ethical while scraping a website and not throttle their servers with requests. Use rests in the code after any successful request to a website.'
Healthy Web Scraping Guide:
1. Better to use API not scraping.
2. Remember to space out the requests.
3. Identify yourself: add a User-Agent string with your information.
"""

"""
1. After fetching html data, I found that data is stored as variable in the script. 
2. I used webdriver to get variable in the script. 
3. Clean and Load data into database.
"""
#agent = driver.execute_script("return navigator.userAgent")
#user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36
opts = Options()
opts.add_argument("user-agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'")
driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=opts)
# directly print the value
driver.get(url)
data = driver.execute_script('return allTyres')
driver.quit()

# connnect database
conn = sqlite3.connect("tyres.db")
c = conn.cursor()
c.execute('''DROP TABLE IF EXISTS tyres''')
c.execute('''CREATE TABLE tyres(website TEXT,tyre_width INT,
    tyre_aspect_ratio INT,tyre_rim_size INT,tyre_brand TEXT,tyre_patten TEXT,tyre_size TEXT,seasonality TEXT,tyre_speed TEXT,price FLOAT)''')
#load data into database
for line in data:
    website =scraped_web 
    tyre_width =width 
    tyre_aspect_ratio =profile 
    tyre_rim_size =rim 
    tyre_brand = line['manufacturer']
    tyre_patten = line['pattern']
    tyre_size = line['description'] # need to change format
    seasonality = "summer" if (line['summer'] == "1" and line['winter']=="0") else "winter" if (line['summer'] == "0" and line['winter']=="1") else "all season"
    tyre_speed = line['speed']
    price = round(float(line['price']),2)
    c.execute('''INSERT INTO tyres VALUES(?,?,?,?,?,?,?,?,?,?)''',(website,tyre_width,
    tyre_aspect_ratio,tyre_rim_size,tyre_brand,tyre_patten,tyre_size,seasonality,tyre_speed,price))
    conn.commit()

print('complete.')
#https://www.bridgestone.co.nz/tyres/learn/understanding-tyre-sizes 
#output to csv
df = pd.read_sql_query("select * from tyres", conn)
df.rename(columns={"price":"price(£)"},inplace=True)
df.to_csv("web1_allTyresData.csv",index=False,encoding='utf-8')
conn.close()