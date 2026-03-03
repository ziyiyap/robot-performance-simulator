import numpy as np
import pandas as pd

def total_distance(df): #takes a dataframe as a parameter
    return round(df['total_distance'].iloc[-1],2)

def average_temperature(df):
    return round(np.mean(df['temperature']),2)

def average_dataframe(df):
    df['chunk'] = df['tick'] //50
    df_tick = df.groupby(['chunk','tick'],as_index = False)[['battery','temperature','x','y']].mean()
    df_chunk = df.groupby(['run_id','chunk'],as_index= False)['malfunction'].sum()
    df_malf_per_chunk = df_chunk.groupby('chunk',as_index=False)['malfunction'].mean()
    df_merged = pd.merge(df_tick,df_malf_per_chunk,on='chunk',how='left')
    return (df_merged,df_malf_per_chunk['malfunction'].sum()) #index 0 is the whole data, index 1 is the sum of the malfunction.

def battery_efficiency(df):
    if df['recharge_count'].iloc[-1] != 0:
        formula = df['tick'].iloc[-1] / df['recharge_count'].iloc[-1]
        return round(formula,2)
    else:
        return df['tick'].iloc[-1]

def longest_stable_run(df):
    stable_streaks = []
    count = 0 
    for x in df['malfunction']:
        if not x:
            count+=1
        else:
            stable_streaks.append(count)
            count = 0
    stable_streaks.append(count)
        
    if len(stable_streaks) != 1:
        return max(stable_streaks)
    else:
        return stable_streaks[0]
