import json
from pprint import pprint
from datetime import datetime
import pandas as pd

# open the json file
# download from:
# https://ec.europa.eu/info/funding-tenders/opportunities/data/referenceData/grantsTenders.json
with open('./grantsTenders.json','r',encoding='utf-8') as f:
    data = json.load(f) 

# extract grants objects
tenderobjs = data['fundingData']['GrantTenderObj']

# Create the pandas dataframe
df = pd.DataFrame(columns=('CallIdentifier','CallTitle','FirstStage','Deadline'))

# Iterate the grands object filling the dataframe with the data of interest
i = 0
for item in tenderobjs:
    try:
        if len(item['deadlineDatesLong']) > 1: # there is two stages in the call
            firstdeadline = datetime.fromtimestamp(item['deadlineDatesLong'][0]/1000).strftime('%d/%m/%Y')
            deadline = datetime.fromtimestamp(item['deadlineDatesLong'][1]/1000).strftime('%d/%m/%Y')
        else: # just one stage
            firstdeadline = 0
            deadline = datetime.fromtimestamp(item['deadlineDatesLong'][0]/1000).strftime('%d/%m/%Y')
        df.loc[i] = [item['callIdentifier'],item['title'],firstdeadline,deadline]
    except:
        pass
    i = i + 1

# Drop dupplicates if any
df = df.drop_duplicates()

# sort the entries cronologicaly
df['Deadline'] = pd.to_datetime(df['Deadline'],format='%d/%m/%Y')
df = df.sort_values(by='Deadline')

# remove the entries older than a give date (e.g. today)
df.drop(df.loc[df['Deadline'] < '2022-02-28 01:00:00'].index, inplace=True)
print(df.head(3))

# export to excel
df.to_excel('eucalls.xlsx',index=False, header = True)