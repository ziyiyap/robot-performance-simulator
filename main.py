import analytics
import os
import time
import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from robot import Robot
from simulation import Simulation

#set base dir to this folder
base_dir = Path(__file__).parent
os.chdir(base_dir)
robots_json = base_dir / 'robots.json'

class UserManager:
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
                self.model = str(input("THERE EXISTS SOME MODELS. CHOOSE YOUR MODEL.\n")).strip().lower()
                for i,data in enumerate(self.robot_data):
                    if self.model in [str(i+1), data['name']]:
                        print(f"LOGGING INTO {data['name']}")
                        self.user_robot = Robot(data['name'],100,26,0,0,data['target'])
                        self.user_simulation = Simulation(self.user_robot) # can be improvised
                        time.sleep(1)
                        #unfinished
                self.user_state = 'user_interface'

    def login(self):
        if self.user_state == 'add_model':
            self.robot_name = str(input("ENTER ROBOT NAME\n"))
            try:
                self.user_target = str(input('ENTER TARGET LOCATION:\n USAGE: <X_COORD>, <Y_COORD>\n')).strip().split(',')
                self.user_target = np.array([[int(self.user_target[0]), int(self.user_target[1])]])
                self.user_robot = Robot(self.robot_name, 100, 26.0, 0, 0,self.user_target)
                json_input = [{
                    'name' : self.user_robot.name,
                    'target' : self.user_robot.target.tolist(),
                    'position' : self.user_robot.position.tolist()
                }]
                with open(robots_json,'w',encoding='utf-8') as file:
                    json.dump(json_input, file)
                print(f"WELL DONE. {self.user_robot.name} HAS BEEN CREATED.")
                self.user_state = 'run_simulation'
                return self.user_state,self.user_robot
            except ValueError or IndexError:
                print('ERROR, PLEASE TRY AGAIN')
                time.sleep(1)
                os.system('cls')
                return
        
        elif self.user_state == 'user_interface':
            os.system('cls')
            self.user_input = str(input("1. Robot Performance Report\n2. Graphs\n3. Run Simulation\n")).lower().strip()
            if self.user_input in ['1','run robot']:
                os.system('cls')
                #check if robot ran any simulations
                if self.user_simulation.count == 0:
                    print(f"{self.user_robot.name} HAS NOT RUN ANY SIMULATIONS.\nROBOT PERFORMANCE REPORT CANNOT BE MADE.")
                    time.sleep(2)
                    return
                else:
                    #report
                    print(f"{'='*5} ROBOT PERFORMANCE REPORT {'='*5}")
                    print(f"{analytics.total_distance(self.user_dataframe)}\n{analytics.average_temperature(self.user_dataframe)}\n{analytics.malfunction_count(self.user_dataframe)}\n{analytics.battery_efficiency(self.user_dataframe)}\n{analytics.longest_stable_run(self.user_dataframe)}")
                    print('='*36)
                    _ = input('')
            elif self.user_input in ['2','graphs']:
                graph_dict = {
                    '1' : (lambda: plt.plot(self.user_dataframe['tick'],self.user_dataframe['battery']), 'Tick', 'Battery Level','Battery Level against Ticks'),
                    '2' : (lambda: plt.plot(self.user_dataframe['tick'],self.user_dataframe['temperature']), 'Tick', 'Temperature', 'Temperature against Ticks'),
                    '3' : (lambda: plt.bar(self.user_dataframe.groupby('chunk')['malfunction'].sum().index, self.user_dataframe.groupby('chunk')['malfunction'].sum().values), 'Chunk', 'Malfunction','Malfunctions per Chunk'),
                    '4' : (lambda: plt.scatter(self.user_dataframe['x'], self.user_dataframe['y']), 'X', 'Y','2D Robot Path')
                }
                os.system('cls')
                self.graph_input = str(input("1. Battery Level against Ticks\n2. Temperature against Ticks\n3. Malfunctions per Chunk\n4. Robot Path\n"))
                if self.graph_input in graph_dict.keys():
                    plt.figure()
                    graph_dict[self.graph_input][0]()
                    plt.xlabel(graph_dict[self.graph_input][1])
                    plt.ylabel(graph_dict[self.graph_input][2])
                    plt.title(graph_dict[self.graph_input][3])
                    plt.grid(True)
                    plt.show()
                else:
                    print('Invalid')
                    time.sleep(1)
                return
            elif self.user_input in ['3','run simulation']:
                self.user_state = 'run_simulation'
                return self.user_state
            
        elif self.user_state == 'run_simulation':
            os.system('cls')
            self.user_simulation = Simulation(self.user_robot)
            self.user_simulation.run()

            #GET DATAFRAME
            self.user_dataframe = self.user_simulation.to_dataframe() 
            time.sleep(2)
            self.user_state = 'user_interface'
            return self.user_state
        

user = UserManager()
while user.status != 'OFFLINE':
    user.login()



#introduction -> simulator -> results
# exists -> extract model -> simulator -> results