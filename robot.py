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
        self.max_battery = 100
    def move(self):
        battery_cost_p_meter = self.max_battery/500
        mean =0
        stdv = 0.5
        global target
        position = np.array([[self.x_position],[self.y_position]])
        steps = 1000
        for i in range(0, steps+1): #if not enough steps, calculate approx how many steps
            #moving mechanism
            noise = np.random.normal(mean,stdv,(2,1))
            remaining = target - position
            #step multiplier
            multiplier = max(1,1+(1.001-1)*((self.battery_level-30)/(self.max_battery-30)))
            step_size = min(np.linalg.norm(remaining) * 0.1 * multiplier,2)
            unit_vector = remaining / np.linalg.norm(remaining)
            new_position = position + noise + step_size * unit_vector
            #small change in position adds to total distance
            delta_position = new_position - position
            dposition_mag = np.linalg.norm(delta_position)
            self.total_distance += dposition_mag
            #stdv change once hit below 40%
            threshold_battery = 40
            if self.battery_level >= threshold_battery:
                stdv = 0.5
            else:
                stdv = max(0.05, 0.5*(self.battery_level/threshold_battery))
            #battery consumption
            battery_consumption = battery_cost_p_meter * np.log(1+dposition_mag)
            self.battery_level = self.battery_level - battery_consumption
            position = new_position
            if np.linalg.norm(remaining)<0.1:
                return f"Reached \n{np.round(position,2)} \nSteps taken: {i+1}\nTotal distance:{round(self.total_distance,2)}\nDisplacement:{round(np.linalg.norm(target),2)}\nBattery: {round(self.battery_level,2)}"
            elif self.battery_level <= 1:
                return f"Low battery. Current location:\n{np.round(position,2)}\nBattery: {round(self.battery_level,2)}"
        return f'Not enough steps!\nCurrent location:\n{np.round(position,2)}\nBattery: {round(self.battery_level,2)}'

jarvis = Robot(100, 30.0, 0, 0, 0.0, 0, 0)

print(jarvis.battery_level)
print(jarvis.move())