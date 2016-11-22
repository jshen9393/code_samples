# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 19:24:20 2016

@author: Jimmy

take downloaded json files from indeed_getjson.py
SQL to create tables
https://app.wagonhq.com/query/26ntiyfj7zxdsalf
https://www.compose.com/articles/using-json-extensions-in-postgresql-from-python-2/

create json table
"""
from indeed_tables import *
from sqlalchemy.sql import exists, insert
from sqlalchemy.exc import IntegrityError
import os
import json
import re


''''
with open ('zip_code_database.csv') as f:
    c = list(csv.reader(f))

for i in range(1,len(c)):
    if len(c[i][2]) < 5:
        c[i][2]='0'*(5-len(c[i][2]))+c[i][2]
    else:
        pass
    print (c[i][2])
    session.add(search_locations(id=None,city=c[i][0],state=c[i][1],zip_code=c[i][2],country=c[i][3],country_code=c[i][4]))

session.commit()
session.close_all()
'''


ld = []      
ld = os.listdir()

#insert or add?

for x in ld:
    b = session.query(exists().where(files.file_name== x)).scalar()
    #the filename check can be moved to try statement
    if '.json' in x and b==False:
        with open(x) as fx:
            j = json.load(fx)
        files_insert = files(file_id=None,file_name = x, query=j['query'],\
        results=len(j['results']),totalresults=int(j['totalResults']))   
        session.add(files_insert)
        session.commit()
        print(x)
        #The file_id was left out as seeing the primary key as integer will automatically increment
        for i in range(1,len(j['results'])):
            jt = j['results'][i]
            q = session.query(files).filter(files.file_name == x ).one()
            try:            
                jobs_insert = jobs(file_id=q.file_id, jobkey=jt['jobkey'], data=jt)
                session.add(jobs_insert)
                session.commit()
                print (jt['jobkey'])
            except IntegrityError:
                session.rollback()
                pass
    session.close_all()
 #session.query(files.file_name,filter(files.file_name = x)
#session.close_all()

'''
for x in ld:
    print (x)
    if '.json' in x:
        with open(x) as fx:
            j = json.load(fx)            
        engine.execute(files.insert(),file_name=x,query=j['query'],\
        results=len(j['results']),totalresults=int(j['totalResults']))
        #The file_id was left out as seeing the primary key as integer will automatically increment
        for i in range(1,len(j['results'])):
            j['results'][i].pop('snippet')
            engine.execute(files.insert(),file_name=x,query=j['query'],\
            results=len(j['results']),totalresults=int(j['totalResults']))
        #session.query(files.file_name,filter(files.file_name = x)
'''
