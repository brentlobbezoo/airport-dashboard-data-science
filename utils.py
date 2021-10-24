def filter_df(df, months=None, origins=None, destinations=None):
    df_copy = df.copy()

    if months:
        df_copy = df_copy[df.Date.dt.month.isin(months)]

    if destinations:
        df_copy = df_copy[df_copy.Dest.isin(destinations)]

    if origins:
        df_copy = df_copy[df_copy.Origin.isin(origins)]

    return df_copy