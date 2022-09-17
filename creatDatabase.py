import sqlite3
import pandas as pd

conn = sqlite3.connect("tyres.db")
c = conn.cursor()

#set up table
"""
c.execute('''CREATE TABLE tyres(website TEXT,tyre_width INT,
    tyre_aspect_ratio INT,tyre_rim_size INT,tyre_brand TEXT,tyre_patten TEXT,tyre_size TEXT,seasonality TEXT,tyre_speed TEXT,price FLOAT)''')

#table2 
c.execute('''CREATE TABLE tyres2(website TEXT,tyre_width INT,
    tyre_aspect_ratio INT,tyre_rim_size INT,tyre_brand TEXT,tyre_patten TEXT,tyre_size TEXT,seasonality TEXT,tyre_review_star FLOAT, tyre_reviews_num FLOAT, price FLOAT)''')"""

conn.close()