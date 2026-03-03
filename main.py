import analytics
import os
import time
import json
import numpy as np
import pandas as pd
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
        self.sim_data = []
        self.time_series_data = []
        self.status = 'ONLINE'
        self.check_user_state() #returns a list of dicts

    def check_user_state(self):
        #checking
        if not robots_json.exists():
            robots_json.touch()
            with open(robots_json,'w',encoding='utf-8') as f:
                json.dump([],f)
            print('JSON FILE CREATED.')
            self.user_state = 'add_model'
            return self.user_state
        elif robots_json.exists():
            try:
                with open(robots_json, encoding='utf-8') as f:
                    self.robot_data = json.load(f) #list of dicts
            except json.JSONDecodeError:
                with open(robots_json,'w',encoding='utf-8') as f:
                    self.robot_data = []
                    json.dump([],f)
            if not self.robot_data:
                print('NO EXISTING MODELS.')
                self.user_state = 'add_model'
                return self.user_state
            else:
                os.system('cls')
                print(f"{'='*30}\n🤖 ROBOT MODEL MANAGER\n{'='*30}\n\n1. Select Existing Model\n2. Create New Model\n3. Remove a Model\n4. Exit\n")
                self.model_manager_choice = str(input("Select >\n")).lower().strip()
                if self.model_manager_choice == '1':
                    return self.cor('create')
                    #
                elif self.model_manager_choice == '2':
                    self.user_state = 'add_model'
                    return self.user_state
                elif self.model_manager_choice == '3':
                    return self.cor('remove')
                elif self.model_manager_choice == '4':
                    self.status = 'OFFLINE'
                    return self.status
                else:
                    return self.check_user_state()
    def model_not_found(self):
        print(f"{self.model} NOT FOUND. PLEASE ENTER A VALID MODEL.".strip())
        time.sleep(1)
        return self.check_user_state()
    
    def cor(self, action): #create or remove
        os.system('cls')
        print(f"{'='*30}\n📂 EXISTING ROBOT MODELS\n{'='*30}\n")
        for i,data in enumerate(self.robot_data):
            print(f"{i+1}. {data['name']} | TARGET: {tuple([data['target'][0][0],data['target'][1][0]])}")
        self.model = str(input("\nSelect model number >\n")).strip()
        if action == 'create':
            for i,data in enumerate(self.robot_data):
                if self.model in [str(i+1), data['name']]:
                    print(f"LOGGING INTO {data['name']}")
                    self.sim_data.clear()
                    self.user_robot = Robot(data['name'],100,0,0,data['target'])
                    self.user_simulation = Simulation(self.user_robot)
                    self.user_state = 'user_interface'
                    time.sleep(1)
                    return self.user_state
            return self.model_not_found()
        elif action == 'remove':
            for i,data in enumerate(self.robot_data):
                if self.model in [str(i+1), data['name']]:
                    print(f"REMOVED {data['name']}")
                    self.robot_data.pop(i)
                    with open(robots_json,'w',encoding='utf-8') as f:
                        json.dump(self.robot_data,f)
                    time.sleep(1)
                    return self.check_user_state()
            return self.model_not_found()

    def login(self):
        os.system('cls')
        if self.user_state == 'add_model':
            with open(robots_json,encoding='utf-8') as f:
                self.robot_data = json.load(f)
            print(f"{'='*30}\n🛠 CREATE NEW ROBOT MODEL\n{'='*30}\n")
            self.robot_name = str(input("ENTER ROBOT NAME > "))
            try:
                if self.robot_name.strip() == '':
                    return self.check_user_state()
                else:
                    self.user_target = str(input('\nENTER TARGET POSITION:\n USAGE: <X_COORD>, <Y_COORD>\n> ')).strip().split(',')
                    self.user_target = np.array([[int(self.user_target[0])], [int(self.user_target[1])]])
            except (ValueError,IndexError):
                print('ERROR, PLEASE TRY AGAIN')
                time.sleep(1)
                os.system('cls')
                return
            self.model_confirmation = str(input('CONFIRM? (Y/N)\n')).strip()
            if self.model_confirmation.lower() == 'y':
                self.user_robot = Robot(self.robot_name, 100, 0, 0,self.user_target)
                self.user_simulation = Simulation(self.user_robot)
                json_input = {
                    'name' : self.user_robot.name,
                    'target' : self.user_robot.target.tolist(),
                    'position' : self.user_robot.position.tolist()
                }

                self.robot_data.append(json_input)
                with open(robots_json,'w',encoding='utf-8') as file:
                    json.dump(self.robot_data, file)
                print(f"\n✅ MODEL {self.user_robot.name} CREATED SUCCESSFULLY.")
                self.user_modelc_choice = str(input("1. Use This Model Now\n2. Back to Main Menu\n")).lower().strip()
                if self.user_modelc_choice in ['1', 'use this model now']:
                    self.user_state = 'run_simulation'
                    return self.user_state,self.user_robot
                else:
                    return self.check_user_state()
            elif self.model_confirmation.lower() == 'n':
                self.user_state = 'add_model'
                return self.user_state
        
        elif self.user_state == 'user_interface':
            #CLI
            print(f"{'=' * 50}\n🤖 ROBOT OPERATIONS CONSOLE\n{'=' * 50}")
            print(f"Model: {self.user_robot.name}\n1. Robot Performance Report\n2. Graphs & Visualisations\n3. Run Simulation\n4. Change Robot Model\n5. Exit\n")
            self.user_input = str(input("Select an option >\n")).lower().strip()
            if self.user_input == '1':
                os.system('cls')
                #check if robot ran any simulations
                if self.user_simulation.count == 0:
                    print(f"{self.user_robot.name} HAS NOT RUN ANY SIMULATIONS.\nROBOT PERFORMANCE REPORT CANNOT BE MADE.")
                    time.sleep(2)
                    return
                else:
                    #takes average of all sims
                    self.average_df = pd.DataFrame(self.sim_data)
                    self.avg_all_sim_df = pd.DataFrame(self.time_series_data) #data of all simulations
                    self.average_data = self.average_df[list(self.average_df.columns)].mean()
                    self.average_data['malfunction_count'] = analytics.average_dataframe(self.avg_all_sim_df)[1]
                    self.average_data = self.average_data.round(2).to_dict()

                    #report
                    self.report_header = f"{'='*5} {self.user_robot.name.upper()} PERFORMANCE REPORT {'='*5}"
                    print(f"{'='*5} {self.user_robot.name.upper()} PERFORMANCE REPORT {'='*5}")
                    print(f"Total Distance Travelled: {self.average_data['total_distance']} units\nAverage Temperature: {self.average_data['average_temp']} °C\nTotal Malfunctions: {self.average_data['malfunction_count']}\nBattery Efficiency: {self.average_data['battery_efficiency']} ticks per charge\nLongest Stable Run: {self.average_data['longest_stable']} ticks")
                    print('='*len(self.report_header))
                    _ = input('')
            elif self.user_input == '2':
                os.system('cls')
                if self.user_simulation.count == 0:
                    print(f"{self.user_robot.name} HAS NOT RUN ANY SIMULATIONS.\nNO GRAPHS OR VISUALISATIONS CAN BE CREATED.")
                    time.sleep(2)
                    return
                else:
                    print(f"{'-' * 30}\n📈 GRAPHS & VISUALIZATIONS\n{'-' * 30}\n1. Single Run\n2. Average Runs\n")
                    self.single_or_avg = str(input("Select > "))
                    if self.single_or_avg == '1':
                        self.graph_df = pd.DataFrame(self.user_dataframe) #gets the latest data
                        self.plot_groupby = self.graph_df.groupby('chunk')['malfunction'].sum()
                        self.plot_chunk, self.plot_malf = self.plot_groupby.index, self.plot_groupby.values
                        
                    elif self.single_or_avg == '2':
                        self._df = pd.DataFrame(self.time_series_data) #data of all simulations
                        self.graph_df = analytics.average_dataframe(self._df)[0]
                        self.plot_chunk, self.plot_malf = self.graph_df['chunk'],self.graph_df['malfunction']


                    else:
                        print("Invalid choice")
                        time.sleep(0.5)
                        return self.user_state
                    os.system('cls')
                    print(f"{'-' * 30}\n📈 GRAPHS & VISUALIZATIONS\n{'-' * 30}\n1. Battery against Ticks\n2. Temperature against Ticks\n3. Malfunctions per Chunk\n4. Robot Path (Y against X)\n")
                    self.graph_input = str(input("Select >\n")).strip()
                    graph_dict = {
                    '1' : (lambda: plt.plot(self.graph_df['tick'],self.graph_df['battery']), 'Tick', 'Battery','Battery against Ticks'),
                    '2' : (lambda: plt.plot(self.graph_df['tick'],self.graph_df['temperature']), 'Tick', 'Temperature', 'Temperature against Ticks'),
                    '3' : (lambda: plt.bar(self.plot_chunk, self.plot_malf), 'Chunk', 'Malfunction','Malfunctions per Chunk'),
                    '4' : (lambda: plt.scatter(self.graph_df['x'], self.graph_df['y']), 'X', 'Y','2D Robot Path')
                }
                    if self.graph_input in graph_dict.keys():

                        plt.figure()
                        graph_dict[self.graph_input][0]()
                        plt.xlabel(graph_dict[self.graph_input][1])
                        plt.ylabel(graph_dict[self.graph_input][2])
                        plt.title(graph_dict[self.graph_input][3])
                        plt.grid(True)
                        plt.show()
                        plt.close()
                    else:
                        print('Invalid')
                        time.sleep(1)
                    return
            elif self.user_input == '3':
                self.user_state = 'run_simulation'
                return self.user_state
            elif self.user_input == '4':
                os.system('cls')
                return self.check_user_state()
            elif self.user_input == '5':
                self.status = 'OFFLINE'
                return self.status
            
        elif self.user_state == 'run_simulation':
            try:
                print(f"{"-"*30}\n🚀 RUN SIMULATION\n{"-"*30}\nSimulation Count: {self.user_simulation.count}\n\n1. Single Run\n2. Multiple Runs (Batch Mode)\n3. Reset Simulation Count\n")
                self.user_sim_count = str(input("Select >\n")).strip().lower()
                if self.user_sim_count == '1':
                    self.user_sim_count = 1
                elif self.user_sim_count == '2':
                    os.system('cls')
                    self.user_sim_count = int(input("Enter number of simulations to run: ").strip())
                elif self.user_sim_count == '3':
                    if self.user_simulation.count != 0:
                        self.time_series_data.clear()
                        self.sim_data.clear()
                        self.user_simulation.count = 0
                        self.user_state = 'user_interface'
                        return self.user_state
                    else:
                        os.system('cls')
                        print("SIMULATION COUNT IS ALREADY CLEARED.")
                        time.sleep(0.5)
                        self.user_state = 'user_interface'
                        return self.user_state
                else:
                    print("Invalid option.")
                    self.user_state = 'user_interface'
                    return self.user_state
            except ValueError:
                self.user_sim_count = 1
            for i in range(1, self.user_sim_count+1):
                self.user_robot.reset()
                self.user_simulation.run()
                #GET DATAFRAME
                self.user_dataframe = self.user_simulation.to_dataframe()
                self.sim_data.append({
                    "total_distance" : analytics.total_distance(self.user_dataframe),
                    "average_temp" : analytics.average_temperature(self.user_dataframe),
                    "battery_efficiency" : analytics.battery_efficiency(self.user_dataframe),
                    "longest_stable" : analytics.longest_stable_run(self.user_dataframe),
                })
                
                for _, row in self.user_dataframe.iterrows():
                    self.time_series_data.append({
                        'run_id' : i,
                        "tick" : row['tick'],
                        "battery" : row['battery'],
                        "temperature" : row['temperature'],
                        'x' : row['x'],
                        'y':row['y'],
                        'malfunction' : row['malfunction']
                    })

            os.system('cls')
            self._ = input(f"Simulation Complete ✅\nTotal Runs: {self.user_sim_count}\n\nEnter any key to continue...\n")
            self.user_state = 'user_interface'
            return self.user_state
        

user = UserManager()
while user.status != 'OFFLINE':
    user.login()