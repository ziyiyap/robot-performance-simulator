import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import seaborn as sns
import time
target = np.array([[100],[20000]])
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
        battery_cost_p_meter = 100 / 500
        td = []
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

            delta_position = new_position - position
            dposition_mag = np.linalg.norm(delta_position)
            td.append(dposition_mag)
            battery_used = battery_cost_p_meter * dposition_mag
            self.battery_level = self.battery_level - battery_used
            position = new_position
            print(self.battery_level)
            if self.battery_level <=0:
                return 'Battery out'
            if np.linalg.norm(remaining)<0.1:
                self.total_distance = sum(td)
                return f"Reached \n{np.round(new_position,2).astype('int')}! Steps taken: {i+1}\n Total distance:{self.total_distance}\nDisplacement:{np.linalg.norm(target)}"
        return 'Not enough steps!'

jarvis = Robot(100, 30.0, 0, 0, 0.0, 0, 0)

print(jarvis.battery_level)
print(jarvis.move())