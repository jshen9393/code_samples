# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 16:42:23 2015

@author: Jimmy

to dos:
can't order the csv columns when converting to dictionary
    1.) can we get the order relating to the dict_key index?
    2.) Would it be better to put it in a pandas dataframe then convert to csv?

The dictionary to csv doesn't work have to find a better way
    1.) a dictionary with multiple items may prove diffcult

database load
    1.) Should the data be converted to csv first or can dictionary be imported into sql database?
"""



import os
import chardet
import re
import csv

folder = 'C:\\in'
infile='test.txt'
outfile = 'test.csv'
encoding = 'UTF-8'

os.chdir(folder)

#Convert input file into utf-8 format
with open(infile,'rb') as file:
    file = file.read()    
    file_encoding = chardet.detect(file)
    file_encoding = file_encoding['encoding']
    if encoding not in file_encoding:
        print('converting file encoding to utf-8')
        data = file.decode(file_encoding).encode(encoding)
    else:
        print('file encoding is utf-8')
        data = file

data = data.decode(encoding)

dict_key_regex = re.compile(r'.+(?<=\t)',re.M)

dict_key = []

for i in dict_key_regex.findall(data):
    if i not in dict_key:
        i=i.strip('\t')
        dict_key.append(i)
    else:
        continue

data_values = []

for d in dict_key:
    values_regex =  re.compile(r'(?<='+re.escape(d)+ '\t).+',re.M)
    values = values_regex.findall(data)
    values = [v.strip('\r') for v in values]
    data_values.append(values)

dictionary = dict(zip(dict_key,data_values))

'''
def WriteDictToCSV(csv_file,csv_columns,dict_data):
    with open(csv_file,'w') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=csv_columns)
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)
    return
 
WriteDictToCSV(outfile,dict_key,dictionary)
#clean up column names for export i=i.replace('\t','').replace(' ','_')
'''