import pandas as pd

def filter_df(df, months=None, origins=None, destinations=None, click_data=None):
    '''
    Filter the dataframe
    '''
    df_copy = df.copy()

    if months:
        df_copy = df_copy[df.Date.dt.month.isin(months)]

    if destinations:
        df_copy = df_copy[df_copy.Dest.isin(destinations)]

    if origins:
        df_copy = df_copy[df_copy.Origin.isin(origins)]

    if click_data:
        print(click_data)

    return df_copy

def clean_df(df):
    '''
    Clean the dataframe of unused columns and optimize
    dataset
    '''
    # Add date as datetime to dataset
    df['Date'] = pd.to_datetime(df.Month.astype(str) + '/' + df.DayofMonth.astype(str) + '/' + df.Year.astype(str))

    # Create a "status" column, idea from "ADRIÁN VERA"
    for dataset in df:
        df.loc[df['ArrDelay'] <= 15, 'Status'] = 'On-time'
        df.loc[df['ArrDelay'] >= 15, 'Status'] = 'Slightly delayed'
        df.loc[df['ArrDelay'] >= 60, 'Status'] = 'Highly delayed'
        df.loc[df['Diverted'] == 1, 'Status'] = 'Diverted'
        df.loc[df['Cancelled'] == 1, 'Status'] = 'Cancelled'

    # Drop columns
    df = df.drop(columns=[
        'Year',
        'Month',
        'DayofMonth',
        'Diverted',
        'Cancelled'
    ])

    return df