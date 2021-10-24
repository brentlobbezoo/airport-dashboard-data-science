import os
import pandas as pd

airports = pd.read_csv(os.path.join(os.getcwd(), 'airports.csv'))

df = pd.read_csv(os.path.join(os.getcwd(), '..', 'data.csv'))

destinations_lat = []
destinations_long = []
origins_lat = []
origins_long = []

for destination in df['Dest']:
    airport = airports[airports.Code.isin([destination])]

    if not airport.empty:
        destinations_lat.append(airport['Lat'].values[0])
        destinations_long.append(airport['Long'].values[0])
    else:
        destinations_lat.append(0)
        destinations_long.append(0)

for origin in df['Origin']:
    airport = airports[airports.Code.isin([origin])]

    if not airport.empty:
        origins_lat.append(airport['Lat'].values[0])
        origins_long.append(airport['Long'].values[0])
    else:
        origins_lat.append(0)
        origins_long.append(0)

df['Dest_Lat'] = destinations_lat
df['Dest_Lng'] = destinations_long
df['Origin_Lat'] = origins_lat
df['Origin_Lng'] = origins_long

df.to_csv('x.csv')