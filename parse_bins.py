# -*- coding: utf-8 -*-
"""
Python 3.5
Gets all bins and parses to tab delimited text
Parsing csv file from github url
"""
import os
import requests
import csv

os.chdir(r'C:\pythonCode\bins')

file = requests.get('https://raw.githubusercontent.com/binlist/data/master/ranges.csv').text

file=file.split('\n')



with open('all_bin.txt','w', newline='') as nf:
    w = csv.writer(nf,delimiter='\t')
    for f in file:
        f = f.split(',')
        if f[1] and f[1] != 'iin_end':
            for i in range(int(f[0]),int(f[1])+1):
                f[0]=i
                f[1]=''
                w.writerow(f)
        else:
            w.writerow(f)


