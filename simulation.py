import pandas as pd

class Simulation:
    def __init__(self,robot):
        self.robot = robot
        self.count = 0
        self.log_data = []
    def run(self):
        self.count +=1
        while self.robot.state != 'DONE': #each loop, 1 tick
            self.log_data.append(self.robot.update())
        return 'DONE'
    def to_dataframe(self):
        df = pd.DataFrame(self.log_data)
        df['chunk'] = df['tick'] // 50
        return df