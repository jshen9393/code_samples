# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 16:42:23 2015

@author: Jimmy

How to convert file encoding
"""
import chardet
import os

os.chdir('c:\\in\\SSPA')
infile = 'water_lat_long.txt'
encoding = 'UTF-8'
outfile = 'converted_'+infile

with open(infile,'rb') as file:
    file = file.read()    
    file_encoding = chardet.detect(file)
    file_encoding = file_encoding['encoding']
    if encoding not in file_encoding: 
        print('converting file encoding to utf-8')
        data = file.decode(file_encoding).encode(encoding)
        with open(outfile, 'w+b') as dest_file:
            contents = file.read()
            dest_file.write(contents.decode(file_encoding).encode(encoding))
    else:
        print('file encoding is utf-8')
        data = file



    