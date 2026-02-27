import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import seaborn as sns
from datetime import datetime
target = np.array([[10000],[20000]])
tick = 0
class Robot:
    def __init__(self, blvl, temp, x,y,totald,malfc,rechargec):
        self.battery_level = blvl
        self.optimum_temp = 60
        self.temp = temp
        self.x_position = x
        self.y_position = y
        self.total_distance = totald
        self.malf_count = malfc
        self.recharge_count = rechargec
        self.max_battery = 100
    def cool_down(self):
        global tick
        while not self.temp < self.optimum_temp:
            self.temp -= 1.5
            tick +=1
        return tick
    def check_malfunction(self, weights=[0.95, 0.05]):
        malfunction_chance = np.random.rand()
        if malfunction_chance < weights[1]:
            self.malf_count +=1
            return True
        else:
            return False
    def recharge(self):
        self.battery_level = self.max_battery
        self.recharge_count+=1
        self.increase_temperature(0, 0.5)
        return self.battery_level 
    def increase_temperature(self,dx, rcharge):
        step_dist_heat = 0.2 * dx
        increment = 0.2 + rcharge + step_dist_heat
        self.temp += increment
        if self.temp >=90:
            self.check_malfunction(weights=[0.55,0.45])
            self.cool_down()
        else:
            self.check_malfunction()
        return self.temp

    def consume_battery(self,dx):
        battery_cost_p_meter = self.max_battery/500
        battery_consumption = battery_cost_p_meter * np.log(1+dx)
        self.battery_level = self.battery_level - battery_consumption
        if self.battery_level <= 20:
            self.recharge()
        return self.battery_level

    def move(self):
        global tick
        mean =0
        stdv = 0.5
        global target
        position = np.array([[self.x_position],[self.y_position]])
        origin = position
        remaining = target - position
        while not np.linalg.norm(remaining)<0.1: #assume 1 step per 5 min
            tick +=1
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
            self.consume_battery(dposition_mag)
            #temp increase
            self.increase_temperature(dposition_mag, 0)
            position = new_position
            if np.linalg.norm(remaining)<0.1:
                return f"Reached \n{np.round(position,2)}\nTotal distance:{round(self.total_distance,2)}\nDisplacement:{round(np.linalg.norm(target-origin),2)}\nBattery: {round(self.battery_level,2)}\nRecharge count:{self.recharge_count}\nTemperature: {self.temp}\nTicks:{tick}"
            elif self.battery_level <= 1:
                return f"Low battery. Current location:\n{np.round(position,2)}\nBattery: {round(self.battery_level,2)}\nTemperature: {self.temp}"

jarvis = Robot(100, 30.0, 0, 0, 0.0, 0, 0)

print(jarvis.battery_level)
print(jarvis.move())