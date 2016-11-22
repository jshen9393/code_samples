# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

https://github.com/eyalzek/price-alert/blob/master/price-alert.py
https://www.youtube.com/watch?v=bhYulVzYRng

open file, load link and price alert
iterate through file to get prices
compare prices
send email if apprpriate

http://www.canadiantire.ca/en/pdp/bauer-vapor-x200-hockey-skates-youth-0836718p.html#srp
"""

from selenium import webdriver

chrome_path = r'C:\Users\Jimmy\Documents\Selenium\chromedriver.exe'

def driver_init(chrome_path,url):
    driver=webdriver.Chrome(chrome_path)
    driver.get(url)
    return driver
    

with open("price_alert.csv") as f:
    r = f.readlines()

    
    
for i in range(len(r)):
    url = r[i].split("\t")[0]
    target_price = r[i].split("\t")[1].strip()
    driver_init(chrome_path,url)
    sale_price = driver.find_element_by_xpath("""/html/body/div[10]/div/div[2]/div/div/section[1]/div/div[1]/div[2]/div/h2/span""")
    regular_price = driver.find_element_by_xpath("""/html/body/div[10]/div/div[2]/div/div/section[1]/div/div[1]/h1/span""")
    item_name = driver.find_element_by_xpath("""/html/body/div[9]/div/div/div[1]/h1""")
    driver.quit()
    with open('results.csv','a') as f:
        f.write(item_name + "\n")
        f.write(sale_price + "\n")
        f.write(regular_price + "\n")
    