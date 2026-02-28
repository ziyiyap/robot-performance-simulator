import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import seaborn as sns
from datetime import datetime


class Robot:
    def __init__(self, blvl, temp, x,y,totald,malfc,rechargec):
        self.target = np.array([[100],[200]])
        self.battery_level = blvl
        self.optimum_temp = 60
        self.temp = temp
        self.x_position = x
        self.y_position = y
        self.position = np.array([[self.x_position],[self.y_position]])
        self.total_distance = totald
        self.malf_count = malfc
        self.last_malfunction = False
        self.recharge_count = rechargec
        self.max_battery = 100
        self.tick = 0
        self.state = 'ACTIVE' #4 states : 'ACTIVE' , 'COOLING' , 'RECHARGING' , 'DONE'
        self.mean =0
        self.stdv = 0.5
        #CONSTANTS
        self.COOLING_RATE = 1.5
        self.TEMP_INCREMENT_FACTOR = 0.2
        self.BATTERY_RATE = 0.25
        self.THRESHOLD_BATTERY = 40
        self.MIN_STDV = 0.05
        self.LOW_POWER_MODE = 20
        self.OVERHEAT = 90
        self.RECHARGE_RATE = 1.8
        self.RECHARGE_HEAT = 0.011
        self.AMBIENT_TEMP = 25

    def cool_down(self):
        self.temp = max(self.temp - self.COOLING_RATE,self.AMBIENT_TEMP)
        return self.temp
    
    def check_malfunction(self, weights=[0.95, 0.05]):
        malfunction_chance = np.random.rand()
        if malfunction_chance < weights[1]:
            self.malf_count +=1
            self.last_malfunction = True
            return self.last_malfunction
        else:
            self.last_malfunction = False
            return self.last_malfunction
        
    def recharge(self):
        self.battery_level += self.RECHARGE_RATE
        self.increase_temperature(0, self.RECHARGE_HEAT)
        return self.battery_level 
    
    def increase_temperature(self,dx, rcharge):
        step_dist_heat = self.TEMP_INCREMENT_FACTOR * dx
        increment = self.TEMP_INCREMENT_FACTOR + rcharge + step_dist_heat
        self.temp += increment
        return self.temp

    def consume_battery(self,dx):
        battery_consumption = self.BATTERY_RATE * np.log(1+dx)
        self.battery_level = self.battery_level - battery_consumption
        return self.battery_level

    def move(self):
        remaining = self.target - self.position #first
        if self.battery_level >= self.THRESHOLD_BATTERY:
            self.stdv = 0.5
        else:
            self.stdv = max(self.MIN_STDV, 0.5*(self.battery_level/self.THRESHOLD_BATTERY))
            
        noise = np.random.normal(self.mean,self.stdv,(2,1)) #noise
        multiplier = max(1,1+(1.05-1)*((self.battery_level-self.LOW_POWER_MODE)/(self.max_battery-self.LOW_POWER_MODE))) #step multiplier
        step_size = min(np.linalg.norm(remaining) * 0.1 * multiplier,2)
        unit_vector = remaining / np.linalg.norm(remaining)
        new_position = self.position + noise + step_size * unit_vector
        #small change in position adds to total distance
        delta_position = new_position - self.position
        dposition_mag = np.linalg.norm(delta_position)
        self.total_distance += dposition_mag
        #battery consumption
        self.consume_battery(dposition_mag)
        #temp increase
        self.increase_temperature(dposition_mag, 0)
        self.position = new_position
        return self.position
    
    def get_status(self, tick):
        log_status = {
            "tick" : tick,
            "battery" : self.battery_level,
            "temperature" : self.temp,
            "x" : self.position[0,0],
            "y" : self.position[1,0],
            "total_distance" : self.total_distance,
            "malfunction" : self.last_malfunction,
            "recharge_count" : self.recharge_count,
            "state" : self.state
        }
        return log_status

    def update(self):
        self.tick +=1
        if self.state == 'ACTIVE':
            self.check_malfunction()
            if np.linalg.norm(self.target - self.position) <0.1:
                self.state = 'DONE'
            elif self.temp >=self.OVERHEAT:
                self.state = 'COOLING'
            elif self.battery_level <= self.LOW_POWER_MODE:
                self.state = 'RECHARGING'
                self.recharge_count +=1
            else:
                self.move()
                            
        elif self.state == 'COOLING':
            self.check_malfunction(weights=[0.90,0.10]) #NOT MALFUNCTION, MALFUNCTION
            self.cool_down()
            if self.temp < self.optimum_temp:
                if self.battery_level <=self.LOW_POWER_MODE:
                    self.state = 'RECHARGING'
                    self.recharge_count +=1
                else:
                    self.state = 'ACTIVE'

        elif self.state == 'RECHARGING':
            self.recharge()
            if self.battery_level >= self.max_battery:
                if self.temp >= self.OVERHEAT:
                    self.state = 'COOLING'
                else:
                    self.state = 'ACTIVE'
        return self.get_status(self.tick)

jarvis = Robot(100, 30.0, 0, 0, 0.0, 0, 0)