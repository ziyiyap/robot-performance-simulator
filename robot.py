import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import seaborn as sns
import time
target = np.array([[100],[200]])
class Robot:
    def __init__(self, blvl, temp, x,y,totald,malfc,rechargec):
        self.battery_level = blvl
        self.temp = temp
        self.x_position = x
        self.y_position = y
        self.total_distance = totald
        self.malf_count = malfc
        self.recharge_count = rechargec
    def move(self):
        global target
        position = np.array([[self.x_position],[self.y_position]])
        steps = 1000
        for i in range(0, steps): #if not enough steps, calculate approx how many steps
            mean =0
            stdv = 0.5
            noise = np.random.normal(mean,stdv,(2,1))
            remaining = target - position
            step_size = np.linalg.norm(remaining) * 0.1
            unit_vector = remaining / np.linalg.norm(remaining)
            new_position = position + noise + step_size * unit_vector
            position = new_position
            if np.linalg.norm(remaining)<0.1:
                return f"Reached \n{np.round(new_position).astype('int')}! Steps taken: {i+1}"
        return 'Not enough steps!'

jarvis = Robot(100, 30.0, 0, 0, 0.0, 0, 0)

print(jarvis.battery_level)
print(jarvis.move())