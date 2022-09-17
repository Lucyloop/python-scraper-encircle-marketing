import sqlite3
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
#set example
width = 205
profile = 55
rim = 16
#web example
scraped_web = "https://www.national.co.uk/"
url = f"https://www.national.co.uk/tyres-search?width={width}&profile={profile}&diameter={rim}&pc=WF26QX"
#scraping
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')
"""
1. After fetching html data, I found that data is stored in the html.
2. I used beautifulsoup and loop to get data in the html. 
"""
# connnect database
conn = sqlite3.connect("tyres.db")
c = conn.cursor()
c.execute('''DROP TABLE IF EXISTS tyres2''')
c.execute('''CREATE TABLE tyres2(website TEXT,tyre_width INT,
    tyre_aspect_ratio INT,tyre_rim_size INT,tyre_brand TEXT,tyre_patten TEXT,tyre_size TEXT,seasonality TEXT,tyre_review_star FLOAT, tyre_reviews_num FLOAT, price FLOAT)''')

# for each tyre result, we insert value into database
all_tyre_results = soup.find_all("div",class_="tyreresult") 
#re1 = re.compile("img/review-scores/star*")
full_star = "img/review-scores/star-full.svg"
half_star = "img/review-scores/star-half.svg"
winter_img = "https://nta.azureedge.net/tyre-fitments/WT.svg"
as_img = "https://nta.azureedge.net/tyre-fitments/AW.svg"
#
for tyre in all_tyre_results:
    website =scraped_web 
    tyre_width =width 
    tyre_aspect_ratio =profile 
    tyre_rim_size =rim 
    tyre_brand =' '.join(tyre.find('img', alt=True)["alt"].split(" ")[0:-1])
    tyre_patten = tyre.find('a', {'class': 'pattern_link'}).text
    tyre_size = ' '.join([i for i in str(tyre.findAll('p')[1]).split(" ") if (i!= '' and i!= '<p>\r\n' and i != '</p>')]).strip()
    # season, acquired based on img label
    all_img_src = [i["src"] for i in tyre.findAll('img')]
    seasonality = "winter" if winter_img in all_img_src else "all season" if as_img in all_img_src else "summer"
    #half star or full star?
    tyre_review_star = float(len([i["src"] for i in tyre.findAll('img') if i["src"]==full_star])+0.5*(1 if half_star in all_img_src else 0))
    tyre_reviews_num = int(tyre.find('a', {'class': 'red'}).text.split(" ")[0])
    price = round(float(tyre.find("span",{"class":"red text-24"}).text.strip()[1:]),2)
    #load intp table
    c.execute('''INSERT INTO tyres2 VALUES(?,?,?,?,?,?,?,?,?,?,?)''',(website,tyre_width,
    tyre_aspect_ratio,tyre_rim_size,tyre_brand,tyre_patten,tyre_size,seasonality,tyre_review_star, tyre_reviews_num,price))
    conn.commit()

print('complete.')

#output to csv
df = pd.read_sql_query("select * from tyres2", conn)
df.rename(columns={"price":"price(£)"},inplace=True)
df.to_csv("web2_allTyresData.csv",index=False,encoding='utf-8')
conn.close()