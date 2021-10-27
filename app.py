import dash
import pandas as pd
import os

from utils import modifier

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Handling DataFrame
df = pd.read_csv(os.path.join(os.getcwd(), 'data2-reduced.csv'))
airports = pd.read_csv(os.path.join(os.getcwd(), 'airports.csv'))

# Filter DataFrame
df = modifier.clean_df(df)

# Extending controls
destinations = pd.unique(df['Dest'].values.ravel())
origins = pd.unique(df['Origin'].values.ravel())
carriers = pd.unique(df['UniqueCarrier'].values.ravel())

destinations.sort()
origins.sort()
carriers.sort()

DESTINATIONS = list(map(lambda x: { 'label': x, 'value': x }, destinations))
ORIGINS = list(map(lambda x: { 'label': x, 'value': x }, origins))
CARRIERS = list(map(lambda x: { 'label': x, 'value': x }, carriers))