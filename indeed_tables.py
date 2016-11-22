# -*- coding: utf-8 -*-
"""
Documentation Used:
https://ads.indeed.com/jobroll/xmlfeed

"""
import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Sequence
from sqlalchemy.dialects.postgresql import JSON, JSONB
from sqlalchemy.sql import exists
from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class api_parameters(Base):
    __tablename__ = 'api_parameters'
    __table_args__ = {"schema": "indeed"}
    #all api fields along with classification ie. default
    api_id = Column(Integer,primary_key=True)
    publisher_id = Column(String(50))
    q = Column(String(50))
    l = Column(String(50))
    sort = Column(String(10))
    st = Column(String(10))
    jt = Column(String(10))
    start = Column(String(5))
    limit = Column(String(5))
    fromage = Column(String(5))
    highlight = Column(String(5))
    filter = Column(String(5))
    latlong = Column(String(1))
    co = Column(String(4))
    chnl = Column(String(10))
    userip = Column(String(50))
    useragent = Column(String(50))
    v = Column(String(1))
    format = Column(String(10))
    config_name = Column(String(50))
    
    def __init__ (self,api_id,publisher_id,q,l,sort,st,jt,start,limit,fromage,highlight,filter,latlong,co,chnl,userip,useragent,v,format,config_name):
        self.api_id = api_id
        self.publisher_id = publisher_id
        self.q = q
        self.l = l
        self.sort = sort
        self.st = st
        self.jt = jt
        self.start = start
        self.limit = limit
        self.fromage = fromage
        self.highlight = highlight
        self.filter = filter
        self.latlong = latlong
        self.co = co
        self.chnl = chnl
        self.userip = userip
        self.useragent = useragent
        self.v = v
        self.format = format
        self.config_name = config_name
    

class search_terms(Base):
    __tablename__ = 'search_terms'
    __table_args__ = {"schema": "indeed"}
    
    term_id = Column(Integer,primary_key=True)
    query = Column(String(256))
    category = Column(String(256))
    project = Column(String(256))
    
    def __init__(self,id,query,category,project):
        self.term_id = term_id
        self.query = query
        self.category = category
        self.project = project
    #search terms, topci and project

class search_locations(Base):
    __tablename__= 'search_locations'
    __table_args__ = {"schema":"indeed"}
    
    location_id = Column(Integer, primary_key=True)
    city = Column(String(256))
    state = Column(String(100))
    zip_code = Column(String(50))
    country = Column(String(256))
    country_code = Column(String(10))
    
    def __init__(self,id,city,state,zip_code,country,country_code):
        self.id = id
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.country_code = country_code


class files(Base):
    __tablename__ = 'files'
    __table_args__ = {"schema":"indeed"}
    
    file_id = Column(Integer,primary_key=True)
    file_name = Column(String(256))
    query = Column(String(256))
    results = Column(Integer)
    totalresults = Column(Integer)

    def __init__(self,file_id,file_name,query,results,totalresults):
        self.file_id = file_id
        self.file_name = file_name
        self.query = query
        self.results = results
        self.totalresults = totalresults

class jobs(Base):
    __tablename__ = 'jobs'
    __table_args__ = {"schema": "indeed"}
    
    file_id = Column(Integer)
    jobkey = Column(String(256),primary_key=True)
    data = Column(JSON)

    def __init__(self,file_id,jobkey,data):
        self.file_id = file_id
        self.jobkey = jobkey
        self.data = data

class lookup_job_titles(Base):
    __tablename__ = 'lookup_job_titles'
    __table_args__ = {"schema": "indeed"}
    
    job_title_id = Column(Integer,primary_key=True)
    job_title_lookup = Column(String(256))
    data = Column(JSON)
    
    def __init__(self,job_title_id,job_title_lookup,data):
        self.job_title_id = job_title_id
        self.job_title_lookup = job_title_lookup
        self.data = data

class mapping_job_titles(Base):
    __tablename__ = 'mapping_job_titles'
    __table_args__ = {"schema": "indeed"}
    
    jobkey = Column(String(256),primary_key=True)
    job_title_mapping = Column(String(256))
    
    def __init__(self,jobkey,job_title_mapping):
        self.jobkey = jobkey
        self.job_title_mapping = job_title_mapping

class mapping_industry(Base):
    __tablename__ = 'mapping_industry'
    __table_args__ = {"schema":"indeed"}
    
    company_id = Column(Integer,primary_key=True)
    company = Column(String(256))
    industry = Column(String(256))
    
    def __init__(self,company_id,company,industry):
        self.company_id = company_id
        self.company = company
        self.industry = industry

class configure(object):
    
    def api_parameters():
        columns = api_parameters.__table__.columns.keys()
        values = {}
        for i in columns:
            if i == 'api_id':
                values[i] = None
            elif i == 'config_name':
                while True:
                    print('enter value for',i)
                    v = input()
                    v = str(v)
                    if session.query(exists().where(api_parameters.config_name==v)).scalar()==False:
                        values[i] = v
                        break
            else:
                print('enter value for',i)
                v = input()
                values[i] = str(v)
        
        conf = api_parameters(api_id=values['api_id'], publisher_id=values['publisher_id'],q=values['q'],l=values['l'],sort=values['sort'],st=values['st'],jt=values['jt'],start=values['start'],limit=values['limit'],fromage=values['fromage'],highlight=values['highlight'],filter=values['filter'],latlong=values['latlong'],co=values['co'],chnl = values['chnl'], userip=values['userip'],useragent=values['useragent'],v=values['v'],format=values['format'],config_name=values['config_name'])   
        session.add(conf)
        session.commit()
        session.close()


db = create_engine('')
engine = db.connect()
meta = MetaData(engine)
session = sessionmaker(bind=engine)
session = session()

'''

with open ('zip_code_database.csv') as f:
    c = list(csv.reader(f))

for i in range(1,len(c)):
    if len(c[i][2]) < 5:
        c[i][2]='0'*(5-len(c[i][2]))+c[i][2]
    else:
        pass
    print (c[i][2])
    session.add(search_locations(id=None,city=c[i][0],state=c[i][1],zip_code=c[i][2],country=c[i][3],country_code=c[i][4]))

session.add(search_locations(id=None,city='remote',state='remote',zip_code='00000',country='remote',country_code='remote'))
session.commit()
session.close_all()
'''
'''
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
'''

