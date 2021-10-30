import os
import pandas as pd

airports = pd.read_csv(os.path.join(os.getcwd(), '..', 'airports.csv'))

df = pd.read_csv(os.path.join(os.getcwd(), '..', 'data.csv'))

df['DestCoords'] = ''
df['OrigCoords'] = ''

for index, row in df.iterrows():
    dest = airports[airports.code.isin([row['Dest']])]
    org = airports[airports.code.isin([row['Origin']])]

    if not dest.empty:
        df.at[index, 'DestCoords'] = dest['coordinates'].values[0]

    if not org.empty:
        df.at[index, 'OrigCoords'] = org['coordinates'].values[0]

df.drop(columns=['Unnamed: 0'])
df.to_csv('data2.csv')