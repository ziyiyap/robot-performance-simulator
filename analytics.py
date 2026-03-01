import numpy as np
import pandas as pd

def total_distance(df): #takes a dataframe as a parameter
    return round(df['total_distance'].iloc[-1],2)

def average_temperature(df):
    return round(np.mean(df['temperature']),2)

def malfunction_count(df):
    return np.sum(df['malfunction'].astype('int'))

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
