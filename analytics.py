from simulation import sim
import numpy as np
import pandas as pd
dataframe = sim.to_dataframe()

def total_distance(df): #takes a dataframe as a parameter
    return f"Total Distance Travelled: {round(df['total_distance'].iloc[-1],2)} units"

def average_temperature(df):
    return f"Average Temperature: {round(np.mean(df['temperature']),2)} °C"

def malfunction_count(df):
    return f"Total Malfunctions: {np.sum(df['malfunction'].astype('int'))}"

def battery_efficiency(df):
    if df['recharge_count'].iloc[-1] != 0:
        formula = df['tick'].iloc[-1] / df['recharge_count'].iloc[-1]
        return f"Battery Efficiency: {round(formula,2)} ticks per charge"
    else:
        return "Maximum efficiency"

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
        return f"Longest Stable Run: {max(stable_streaks)} ticks"
    else:
        return f'No malfunctions! {stable_streaks[0]} ticks'
