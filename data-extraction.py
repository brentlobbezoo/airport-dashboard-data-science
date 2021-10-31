import pandas as pd
import os

# Handling DataFrame
df = pd.read_csv(os.path.join(os.getcwd(), 'data', 'data2.csv'))

# Fetch all cancelled and use DataFrame as base
cancelled = df[df.Cancelled == 1]

# Fetch all not cancelled
not_cancelled = df[df.Cancelled == 0]

for month in range(1, 13):
    results = not_cancelled[not_cancelled.Month == month]
    cancelled = cancelled.append(results.sample(n=10000))

cancelled.to_csv('data-reduced.csv')