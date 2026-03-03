import numpy as np
import pandas as pd

def total_distance(df): #takes a dataframe as a parameter
    return round(df['total_distance'].iloc[-1],2)

def average_temperature(df):
    return round(np.mean(df['temperature']),2)

def average_dataframe(df):
    df['chunk'] = df['tick'] //50 #creates a new column called chunk
    df_tick = df.groupby(['chunk','tick'],as_index = False)[['battery','temperature','x','y']].mean() #'chunk' is included so we can merge later. [['battery','temperature','x','y']] takes the average per tick per simulation.
    df_chunk = df.groupby(['run_id','chunk'],as_index= False)['malfunction'].sum()  # malfunction sums based on the sim index (run_id) and chunk. Ex. Chunk 0s of sim 1 ,sim 2 and the rest of the simulation sum together, Chunk 1s of sim 1 and sim 2 and the rest of the simulation sum together
    df_malf_per_chunk = df_chunk.groupby('chunk',as_index=False)['malfunction'].mean() #now it means according to how many simulations.
    df_merged = pd.merge(df_tick,df_malf_per_chunk,on='chunk',how='left') #merges two dataframes, common column as ['chunk']
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
