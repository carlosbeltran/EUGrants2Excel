import json
from pprint import pprint
from datetime import datetime
import pandas as pd

with open('./grantsTenders.json','r',encoding='utf-8') as f:
    data = json.load(f) 

tenderobjs = data['fundingData']['GrantTenderObj']
df = pd.DataFrame(columns=('CallIdentifier','CallTitle','Deadline'))
i = 0
for item in tenderobjs:
    try:
        #deadline = datetime.fromtimestamp(item['deadlineDatesLong'][0]/1000).strftime('%d/%m/%Y %H:%M:%S')
        deadline = datetime.fromtimestamp(item['deadlineDatesLong'][0]/1000).strftime('%d/%m/%Y')
        #print(f"{item['callIdentifier']} {item['callTitle']} {deadline}")
        df.loc[i] = [item['callIdentifier'],item['title'],deadline]
    except:
        pass
    i = i + 1

df = df.drop_duplicates()
df['Deadline'] = pd.to_datetime(df['Deadline'],format='%d/%m/%Y')
df = df.sort_values(by='Deadline')
print(df.head(3))

df.to_excel('eucalls.xlsx',index=False, header = True)