# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 18:13:49 2016

@author: Jimmy
"""
from indeed_tables import Base,search_locations,api_parameters,session,configure
from sqlalchemy import distinct
import requests
import json
import time
import math
import csv

'''
get.() has parameter function that can pass queries
http://docs.python-requests.org/en/master/user/quickstart/#make-a-request
http://www.unitedstateszipcodes.org/zip_code_database.csv
'''
def api_dict(search,add_new=False,config='default'):    
    if add_new:
        configure.api_parameters()
    else:
        a = api_parameters
        d = session.query(a.publisher_id,a.q,a.l,a.sort,a.st,a.jt,a.start,a.limit,a.fromage,a.highlight,a.filter,a.latlong,a.co,a.chnl,a.userip,a.useragent,a.v,a.format).filter(a.config_name == config).one()
        r = api_parameters.__table__.columns.keys()
        r.pop(0)
        r.pop(-1)
        v = {}
        for i in range(len(r)):
            v[r[i]] = d[i]
        v['publisher'] = v['publisher_id']    
        v['q'] = search
        return v


def api_results(d):
    url = 'http://api.indeed.com/ads/apisearch?'
    j = requests.get(url,params=d).json()
    return j

def write_file(d,j): 
    file = str(time.strftime("%Y%m%d") + '_' + str(d['q'].replace(' ','_'))+'_'+str(str(d['l']).replace(', ','_'))+'_'+str(j['start'])+'-'+str(j['end'])+'.json')
    print(file)
    with open(file,'w') as f:
        json.dump(j,f,ensure_ascii=True) #to string

def loops(j):
    if j['totalResults'] == 0:
        return 0, j['totalResults']
    elif j['totalResults'] > 1024:
        return math.ceil(1025/int(d['limit'])),j['totalResults']
    else:
        return math.ceil(j['totalResults']/int(d['limit'])), j['totalResults']

class region(object):  
    all_states = session.query(distinct(search_locations.state)).all()
    all_cities = session.query(search_locations.city, search_locations.state).group_by(search_locations.city, search_locations.state).all()
    all_zip_codes = session.query(distinct(search_locations.zip_code)).all()
    
    def city_by_state(state):
        s = search_locations
        cities = session.query(s.city, s.state).group_by(s.city,s.state).filter(s.state==state).all()
        return cities
    def zip_by_city(city,state):
        s = search_locations
        zip_codes = session.query(s.zip_code).group_by(s.zip_code).filter(s.state==state,s.city==city).all()
        return zip_codes
        
def results_logic(d,j):
    l = loops(j)
    if l[1] == 0:
        pass
    else:
        
        for x in range(l[0]):
            if x == 0:
                d['start'] = '0'             
            else:     
                d['start'] = j['end']
            j=api_results(d)
            write_file(d,j)
            
def big_results(d):
        s = region.all_states
        for x in s:
            print('searching',x)
            d['l'] = ''.join(x)
            j = api_results(d)
            if loops(j)[1] > 1000:
                c = region.city_by_state(x)
                for y in range(len(c)):
                    print('searching', c[y])
                    d['l'] = c[y][0]+', '+c[y][1]
                    j = api_results(d)
                    results_logic(d,j)
            results_logic(d,j)
#as_and=data+scientist&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=            

d = api_dict('data scientist')
j = api_results(d)

l = loops(j)
if l[1] == 0:
    pass
elif l[1] > 1000:
    big_results(d)
else:
    results_logic(d,j)
            
'''          
d={}
d['publisher'] = r[1][0]# indeed publisher id
d['q']= 'tibco'#r[1][1]#search
d['l'] = location(r[1][2]) #zip code or 'city, state'
d['sort'] = r[1][3] #relevance or date
d['radius'] = r[1][4] #default is 25 miles
d['st'] = ''# 'jobsite' for only job boards 'employer' for employer websites
d['jt'] = '' #job type fulltime, parttime, contract, internship, temporary
d['start']='0' #start results at this number. default is 0
d['limit']= '25' #max number of results, default is 10, 25 is max
d['fromage']= '1000' #of days back to search
d['highlight']='' #see documentation.  formatting of results
d['filter'] = '' #turn off duplicate results. default is 1
d['latlong'] = '1' #retuns lat and long of result.  Default is 0
d['co'] = 'us' #country
d['chnl'] ='' #channel name for group requests
d['userip'] = '2600:8806:a500:219:1064:7cfb:ead6:35a3'
#v = 2 (version2) and format=json are all hard coded
#d['useragent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
#makesure formating is ok
'''


'''
with open('search.csv') as f:
s = list(csv.reader(f))

for x in s:
    d['start'] = '0'
    d['l'] = ''
    d['q'] = ''.join(x)
    j = api_results(d)
    l = loops(j)
    if l[1] == 0:
        pass
    elif l[1] > 1000:
        big_results(d)
    else:
        results_logic(d,j)
x = 'data scientist'
d['start'] = '0'
d['l'] = ''
d['q'] = ''.join(x)
d['publisher'] = '9551346561875460'
j = api_results(d)

l = loops(j)
if l[1] == 0:
    pass
elif l[1] > 1000:
    big_results(d)
else:
    results_logic(d,j)
'''
