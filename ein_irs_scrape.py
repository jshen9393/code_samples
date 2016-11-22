# -*- coding: utf-8 -*-
"""
This is a logic to scrape the IRS website for non-profit information

Command line arguments:
first argument is the input file and the second is output file.  There are default settings if args are not used.

The infile should only consist of the an ein number with a newline break and a header.

The outfile is will be formatted as such:
['ein','name','city','state','country','status']

"""
import sys
import requests
import bs4 
import os
import csv

def csv_writeline(file,line):
    with open(file,'a',newline='') as f:
        w = csv.writer(f,delimiter='\t')
        w.writerow(line)

in_file = sys.argv[1]
out_file = sys.argv[2]


header = ['ein','name','city','state','country','status']

csv_writeline(out_file,header)


with open(in_file) as f:
    f = f.readlines()
f.pop(0)


for ein in f:
    ein = ein.strip()
    if len(ein) < 9: #EIN has to be at least 9 characters
        pass
    else:
        url='https://apps.irs.gov/app/eos/pub78Search.do?ein1={0}&names=&city=&state=All...&country=US&deductibility=all&dispatchMethod=searchCharities&submitName=Search'.format(ein)
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.text,'html.parser')
        rows = soup.find_all('tr')
        try:
            info = rows[3].find_all('td')
            p_ein = info[0].text.strip().replace('-','')
            p_name= info[1].text.strip()
            p_city= info[2].text.strip()
            p_state= info[3].text.strip()
            p_country= info[4].text.strip()
            p_status= info[5].text.strip().replace(',',' ')
            rowlist = [p_ein,p_name,p_city,p_state,p_country,p_status]
            csv_writeline(out_file,rowlist)
            print(ein,'completed')
        except:
            print(ein,'error')
            pass

    