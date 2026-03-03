import analytics
from robot import Robot
import os
import time
import json
import numpy as np
import matplotlib.pyplot as plt
from simulation import Simulation
from pathlib import Path

#set base dir to this folder
base_dir = Path(__file__).parent
os.chdir(base_dir)
robots_json = base_dir / 'robots.json'

class Login:
    def __init__(self):
        self.status = 'ONLINE'
        if not robots_json.exists():
            robots_json.touch()
            self.user_state = 'add_model'
        elif robots_json.exists():
            with open(robots_json,encoding='utf-8') as f:
                self.content = f.read().strip()
            if not self.content:
                self.user_state = 'add_model'
            else:
                with open(robots_json, encoding='utf-8') as f:
                    self.robot_data = json.load(f)
                for i,data in enumerate(self.robot_data):
                    print(f"{i+1}. {data['name']}")
                model = str(input("THERE EXISTS SOME MODELS. CHOOSE YOUR MODEL.\n")).strip().lower()
                for i,data in enumerate(self.robot_data):
                    if model in [str(i+1), data['name']]:
                        print(f"LOGGING INTO {data['name']}")
                        time.sleep(2)
                self.user_state = 'user_interface'
    def login(self):
        if self.user_state == 'add_model':
            robot_name = str(input("ENTER ROBOT NAME\n"))
            try:
                self.user_target = str(input('ENTER TARGET LOCATION:\n USAGE: <X_COORD>, <Y_COORD>\n')).strip().split(',')
                self.user_target = (int(self.user_target[0]), int(self.user_target[1]))
                user_robot = Robot(robot_name, 100, 26.0, 0, 0,self.user_target)
                json_input = [{
                    'name' : user_robot.name,
                    'target' : user_robot.target.tolist(),
                    'position' : user_robot.position.tolist()
                }]
                with open(robots_json,'w',encoding='utf-8') as file:
                    json.dump(json_input, file)
                print(f"WELL DONE. {user_robot.name} HAS BEEN CREATED.")
            except ValueError or IndexError:
                print('ERROR, PLEASE TRY AGAIN')
                time.sleep(1)
                os.system('cls')
                return
            #SIMULATOR
            user_simulation = Simulation(user_robot)
            user_simulation.run()

            #GET DATAFRAME
            user_dataframe = user_simulation.to_dataframe() 
            time.sleep(2)
            self.user_state = 'user_interface'
            return self.user_state
        elif self.user_state == 'user_interface':
            os.system('cls')
            user_input = str(input("1. Robot Performance Report\n2. Graphs\n")).lower().strip()
            if user_input in ['1','run robot']:
                os.system('cls')
                #report
                print(f"{'='*5} ROBOT PERFORMANCE REPORT {'='*5}")
                print(f"{analytics.total_distance(user_dataframe)}\n{analytics.average_temperature(user_dataframe)}\n{analytics.malfunction_count(user_dataframe)}\n{analytics.battery_efficiency(user_dataframe)}\n{analytics.longest_stable_run(user_dataframe)}")
                print('='*36)
                s = input('')
            elif user_input in ['2','graphs']:
                graph_dict = {
                    '1' : (lambda: plt.plot(user_dataframe['tick'],user_dataframe['battery']), 'Tick', 'Battery Level','Battery Level against Ticks'),
                    '2' : (lambda: plt.plot(user_dataframe['tick'],user_dataframe['temperature']), 'Tick', 'Temperature', 'Temperature against Ticks'),
                    '3' : (lambda: plt.bar(user_dataframe.groupby('chunk')['malfunction'].sum().index, user_dataframe.groupby('chunk')['malfunction'].sum().values), 'Chunk', 'Malfunction','Malfunctions per Chunk'),
                    '4' : (lambda: plt.scatter(user_dataframe['x'], user_dataframe['y']), 'X', 'Y','2D Robot Path')
                }
                os.system('cls')
                graph_input = str(input("1. Battery Level against Ticks\n2. Temperature against Ticks\n3. Malfunctions per Chunk\n4. Robot Path\n"))
                if graph_input in graph_dict.keys():
                    plt.figure()
                    graph_dict[graph_input][0]()
                    plt.xlabel(graph_dict[graph_input][1])
                    plt.ylabel(graph_dict[graph_input][2])
                    plt.title(graph_dict[graph_input][3])
                    plt.grid(True)
                    plt.show()
                else:
                    print('Invalid')
                    time.sleep(1)
                return
        

user = Login()
while user.status != 'OFFLINE':
    user.login()



#introduction -> simulator -> results
# exists -> extract model -> simulator -> results