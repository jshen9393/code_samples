# -*- coding: utf-8 -*-
"""

Data Source:
http://nflsavant.com/pbp_data.php?year=2015

"""
import os
import pandas as pd
import numpy as np
from pandas import DataFrame
import re


#file location
file_loc = '[file directory]'
os.chdir(file_loc)

file = 'pbp-2015.csv'
data = pd.read_csv(file)
df = DataFrame(data)


#Remove blank columns as they are useless and can damage other processes
columns = df.columns.values

deleted_columns = []

for c in columns:
    values = pd.unique(df[c])   
    if len(values) == 1 and np.isnan(values).any():
        deleted_columns = deleted_columns
        deleted_columns.append(c)
        df = df.drop([c],axis=1)

    else:
        pass

print(deleted_columns, 'deleted')
'''
There is no sequential playid in a game. Important for finding results
from one play to the other such as net yards gain.
The quarter, minute, and second fields will be used to generate
an ascending playid key.
Quarters ascend with time but minutes and seconds do not.
These will be reversed so the playid can be in sequence.
'''
second = np.arange(0,60)
second_rev = second[::-1]
seconddict = dict(zip(second, second_rev.T))

minute = np.arange(0,16)
minute_rev = minute[::-1]
minutedict = dict(zip(minute, minute_rev.T))

#no play items will duplicate time records
#Must add value only if value is null

df['TimeFlag'] = '0'

df.loc[df['PlayType'] == 'KICKOFF','TimeFlag'] = '1'
df.loc[df['PlayType'] == 'NO PLAY','TimeFlag'] = '1'
df.loc[df['PlayType'] == 'TIMEOUT','TimeFlag'] = '1'
df.loc[df['PlayType'].isnull(),'TimeFlag'] = '1'
df.loc[df['PlayType'] == 'EXTRA POINT','TimeFlag'] = '1'
#df['TimeFlag'].fillna('0',inplace=True)


#df['PlayId'] = str(df['GameId']) + str(df['Quarter']) + str((df['Minute'].map(minutedict).zfill(2)) + str(df['Second'].map(seconddict)).zfill(2)

df['PlayId'] = df['GameId'].astype(str)\
 + df['Quarter'].astype(str)\
 + df['Minute'].map(minutedict).apply('{:0>2}'.format) \
 + df['Second'].map(seconddict).apply('{:0>2}'.format) \
 + df['TimeFlag'].astype(str)
 #(?:(?<=^HEADa\b)|(?<=\bHEAD\b))
#Identify players from description column


#Scanning through data, the pass_type has some errant data.

#passes that lack pass location will default on short middle
df.loc[df['PlayId']=='2015111504411450','PassType']='SHORT MIDDLE'
df.loc[df['PlayId']=='2015113000313520','PassType']='SHORT RIGHT'
df.loc[df['PlayId']=='2015120700209150','PassType']='SHORT MIDDLE'
df.loc[df['PlayId']=='2015121300100590','PassType']='SHORT LEFT'
df.loc[df['PlayId']=='2015121302408220','PassType']='DEEP LEFT'
df.loc[df['PlayId']=='2016010310309240','PassType']='SHORT MIDDLE'
df.loc[df['PlayId']=='2015091308308040','PassType']='SHORT MIDDLE'
df.loc[df['PlayId']=='2015092400114260','PassType']='DEEP RIGHT'
df.loc[df['PlayId']=='2015092703403450','PassType']='DEEP LEFT'
df.loc[df['PlayId']=='2015092707213590','PassType']='SHORT LEFT'
df.loc[df['PlayId']=='2015092708307430','PassType']='SHORT LEFT'
df.loc[df['PlayId']=='2015092710215170','PassType']='DEEP RIGHT'
df.loc[df['PlayId']=='2015101111415090','PassType']='DEEP MIDDLE'
df.loc[df['PlayId']=='2015101500309020','PassType']='SHORT MIDDLE'
df.loc[df['PlayId']=='2015101800215010','PassType']='SHORT MIDDLE'
df.loc[df['PlayId']=='2015102509305450','PassType']='SHORT MIDDLE'
df.loc[df['PlayId']=='2015102509305580','PassType']='SHORT MIDDLE'
df.loc[df['PlayId']=='2015102511106440','PassType']='DEEP LEFT'
df.loc[df['PlayId']=='2015110801412160','PassType']='SHORT RIGHT'
df.loc[df['PlayId']=='2015111500410140','PassType']='DEEP LEFT'
df.loc[df['PlayId']=='2015111502410110','PassType']='SHORT MIDDLE'
df.loc[df['PlayId']=='2015111510101500','PassType']='SHORT MIDDLE'
df.loc[df['PlayId']=='2015112202106290','PassType']='DEEP MIDDLE'
df.loc[df['PlayId']=='2015112300210280','PassType']='SHORT MIDDLE'
df.loc[df['PlayId']=='2015112601408040','PassType']='SHORT MIDDLE'
df.loc[df['PlayId']=='2015113000103300','PassType']='SHORT MIDDLE'
df.loc[df['PlayId']=='2015113000204320','PassType']='SHORT LEFT'
df.loc[df['PlayId']=='2015120300114570','PassType']='SHORT MIDDLE'
df.loc[df['PlayId']=='2015120613111480','PassType']='SHORT LEFT'
df.loc[df['PlayId']=='2015121000215380','PassType']='SHORT MIDDLE'
df.loc[df['PlayId']=='2015121300403020','PassType']='DEEP LEFT'
df.loc[df['PlayId']=='2015121700113570','PassType']='SHORT MIDDLE'
df.loc[df['PlayId']=='2015122704411050','PassType']='SHORT MIDDLE'
df.loc[df['PlayId']=='2015122800506060','PassType']='SHORT MIDDLE'
df.loc[df['PlayId']=='2015112910414140','PassType']='DEEP RIGHT'
df.loc[df['PlayId']=='2015121305201200','PassType']='DEEP RIGHT'
df.loc[df['PlayId']=='2015122400214210','PassType']='SHORT MIDDLE'
df.loc[df['PlayId']=='2016010311112050','PassType']='SHORT MIDDLE'


pass_type_error = ['INTENDED FOR', 'RIGHT TO',
       '(6:44) (SHOTGUN)', 'LEFT TO', 'PASS RULING,', '(13:19) 5-TTAYLOR',
       'IN 119', 'INTERCEPTED BY', 'NOT LISTED', '(10:14) 17-PRIVERS',
       '(10:01) (SHOTGUN)', '[20-C.GRAHAM]. THROWN', 'MIDDLE TO',
       '[55-S.TULLOCH]. PENALTY', '(:21) 5-TBRIDGEWATER',
       '[31-M.ALEXANDER]. PENALTY', '(4:54) 2-JMANZIEL',
       '[58-V.MILLER]. THE']

 
for p in pass_type_error:
    df.loc[df['PassType']== p,'DataError'] = 'error' 
    
df.loc[(df['PlayType']=='PASS') & (df['DataError']!='error') & (df['PassType'].isnull()),'DataError'] = 'error'



'''

Adding Additional Data Points

'''

#Passer/Quarterback
df.loc[(df['PlayType']=='PASS'),'Passer'] = df['Description'].str.extract('(\d+\-[A-Z]\.[A-Z]+(?=\sPASS))').astype(str)

#Receiver

pass_type = pd.unique(df[(df['PlayType']=='PASS') & (df['DataError']!='error')]['PassType'])

for p in pass_type:
    regex = p.replace(' ','\s')
    #completed pass
    df.loc[(df['PlayType']=='PASS') & (df['IsInterception']==0) &\
    (df['IsIncomplete']==0)& (df['PassType']==p),'Receiver']\
    = df['Description'].str.extract('((?<=PASS\s'+regex+'\sTO\s)\d+\-[A-Z]\.[A-Z]+)').astype(str)
    #incompleted pass
    df.loc[(df['PlayType']=='PASS') & (df['IsInterception']==0) &\
    (df['IsIncomplete']==1)& (df['PassType']==p),'Receiver']\
    = df['Description'].str.extract('((?<=PASS\sINCOMPLETE\s'+regex+'\sTO\s)\d+\-[A-Z]\.[A-Z]+)').astype(str)
    #intercepted pass
    df.loc[(df['PlayType']=='PASS') & (df['IsInterception']==1) &\
    (df['PassType']==p),'Receiver']\
    = df['Description'].str.extract('((?<=PASS\s'+regex+'\sINTENDED\sFOR\s)\d+\-[A-Z]\.[A-Z]+)').astype(str)
    

#Rusher

formation = ['NO HUDDLE, SHOTGUN', 'NO HUDDLE','SHOTGUN']
#shotgun and no huddle formations

for f in formation:
    f1 = f.replace(',','')
    regex = f.replace(' ','\s') 
    df.loc[(df['PlayType']=='RUSH')  & (df['Formation']==f1) &\
    (df['DataError'].isnull()),'Rusher']=df['Description'].str.extract('((?<='+regex +'\)\s)\d+\-[A-Z]\.[A-Z]+)').astype(str)
else:
    pass



#under center formations

df.loc[(df['PlayType']=='RUSH') & (df['Formation']=='UNDER CENTER') &\
(df['DataError'].isnull()),'Rusher']=df['Description'].str.extract('((?<=\)\s)\d+\-[A-Z]\.[A-Z]+)').astype(str)

#field goal, only one record
df.loc[(df['PlayType']=='RUSH') & (df['Formation']=='FIELD GOAL') &\
(df['DataError'].isnull()),'Rusher'] = '9-M.STAFFORD'

#QB Scramble
df.loc[(df['PlayType']=='SCRAMBLE') &\
(df['DataError'].isnull()),'Rusher']=df['Description'].str.extract('(\d+\-[A-Z]\.[A-Z]+(?=\sSCRAMBLES))').astype(str)

#manual cleanse for players
df.loc[df['PlayId']=='2015122707203030','Rusher']='35-M.TOLBERT'
df.loc[df['PlayId']=='2015121311412140','Rusher']='28-L.MURRAY'
df.loc[df['PlayId']=='2015111510101500','Receiver']='80-V.DAVIS'
df.loc[df['PlayId']=='2015111510213030','Receiver']='UNKNOWN'
df.loc[df['PlayId']=='2015092000415370','Receiver']='UNKNOWN'
df.loc[df['PlayId']=='2015100406114320','Receiver']='UNKNOWN'
df.loc[df['PlayId']=='2015100406411490','Receiver']='UNKNOWN'
df.loc[df['PlayId']=='2015112601408040','Receiver']='UNKNOWN'
df.loc[df['PlayId']=='2015122707205400','Receiver']='UNKNOWN'
df.loc[df['PlayId']=='2015120611300590','Receiver']='97-M.JACKSON'
df.loc[df['PlayId']=='2015110809311020','Receiver']='UNKNOWN'
df.loc[df['PlayId']=='2015120611412300','Receiver']='UNKNOWN'
df.loc[df['PlayId']=='2015122800506060','Receiver']='UNKNOWN'


#IsComplete flag
df.loc[(df['IsPass']==1) & (df['IsInterception']==0) & (df['IsIncomplete']==0),'IsComplete']= 1
df.loc[(df['IsPass']==1) & (df['IsInterception']==1) & (df['IsIncomplete']==0),'IsComplete']= 0
df.loc[(df['IsPass']==1) & (df['IsInterception']==0) & (df['IsIncomplete']==1),'IsComplete']= 0
df.loc[(df['IsPass']==0),'IsComplete']= 0



#exports results to a csvfile
'''
with open('nfl_plays_cleaned.csv','w') as file:
    df.to_csv(file)
'''  
