import graph_processing as gp
import power_flow_processing as pfp
import power_system_simulation as pss
import pandas as pd
import numpy as np

# write exceptions here


class PowerSim:
    def __init__(self, grid_data: dict) -> None:
        self.PowerSimModel = pfp.PowerFlow(grid_data=grid_data)

    def example_code(self):
        print("Who reads trek een bak")

    def n1_calculations():
        pass

    def ev_penetration():
        pass

    def optimal_tap_position(self, active_power_profile_assign3: pd.DataFrame, reactive_power_profile_assign3: pd.DataFrame) -> pd.DataFrame:

        # PowerSim saves the model as PowerSimModel
        # access to assignment 2 functions is now given as 
        output_data = self.PowerSimModel.batch_powerflow(active_power_profile=active_power_profile_assign3, reactive_power_profile=reactive_power_profile_assign3)

        tap_position = 0
        tap_size_procent = self.PowerSimModel.grid_data['transformer']['tap_size']/self.PowerSimModel.grid_data['transformer']['u1']*100

        if(self.PowerSimModel.grid_data['transformer']['tap_min'] > self.PowerSimModel.grid_data['transformer']['tap_max']): # tap_min > tap_max
            number_of_taps_non_min = self.PowerSimModel.grid_data['transformer']['tap_min']-self.PowerSimModel.grid_data['transformer']['tap_nom']
            number_of_taps_non_max = self.PowerSimModel.grid_data['transformer']['tap_nom']-self.PowerSimModel.grid_data['transformer']['tap_max']
            number_of_taps_min_max = self.PowerSimModel.grid_data['transformer']['tap_min']-self.PowerSimModel.grid_data['transformer']['tap_max']
        else: #tap_min < tap_max
            number_of_taps_non_max = self.PowerSimModel.grid_data['transformer']['tap_max']-self.PowerSimModel.grid_data['transformer']['tap_nom']
            number_of_taps_non_min = self.PowerSimModel.grid_data['transformer']['tap_nom']-self.PowerSimModel.grid_data['transformer']['tap_min']
            number_of_taps_max_min = self.PowerSimModel.grid_data['transformer']['tap_max']-self.PowerSimModel.grid_data['transformer']['tap_min']

        for i in range(len(output_data["node"]["id"])):
            if isinstance(output_data["node"]["id"][i], (list, np.ndarray)):
                for j in range(len(output_data["node"]["id"][i])):
                    if output_data["node"]["id"][i][j] == self.PowerSimModel.grid_data['transformer']['from_node']:
                        # Calculating the tap_procent
                        tap_procent = ((output_data["node"]["u"][i][j]-self.PowerSimModel.grid_data['transformer']['u1'])/(self.PowerSimModel.grid_data['transformer']['u1']))*100


                        if((self.PowerSimModel.grid_data['transformer']['tap_min'] > self.PowerSimModel.grid_data['transformer']['tap_max'])):
                            if tap_procent > 0:
                                for k in range(number_of_taps_non_max[0]+1):
                                    if (((0.5+k)*tap_size_procent) > tap_procent):
                                        tap_position1 = self.PowerSimModel.grid_data['transformer']['tap_nom'] + k
                                        tap_position = tap_position + tap_position1[0]
                                        break
                            else:
                                for k in range(number_of_taps_non_max[0]+1):
                                    if (((0.5+k)*tap_size_procent) > tap_procent):
                                        tap_position1 = self.PowerSimModel.grid_data['transformer']['tap_nom'] - k
                                        tap_position = tap_position + tap_position1[0]
                                        break
                        elif((self.PowerSimModel.grid_data['transformer']['tap_min'] < self.PowerSimModel.grid_data['transformer']['tap_max'])):
                            if tap_procent > 0:
                                for k in range(number_of_taps_non_max[0]+1):
                                    if (((0.5+k)*tap_procent) > tap_procent):
                                        tap_position1 = self.PowerSimModel.grid_data['transformer']['tap_nom'] - k
                                        tap_position = tap_position + tap_position1[0]
                                        break
                            else:
                                for k in range(number_of_taps_non_max[0]+1):
                                    if (((0.5+k)*tap_procent) > tap_procent):
                                        tap_position1 = self.PowerSimModel.grid_data['transformer']['tap_nom'] + k
                                        tap_position = tap_position + tap_position1[0]
                                        break
                        

        optimial_tap_position = tap_position/(len(output_data["node"]["id"]))
        if(self.PowerSimModel.grid_data['transformer']['tap_max'] < self.PowerSimModel.grid_data['transformer']['tap_min']):
            for i in range(number_of_taps_min_max[0]):
                if((self.PowerSimModel.grid_data['transformer']['tap_max'])+i-0.5<tap_position and (self.PowerSimModel.grid_data['transformer']['tap_max'])+i+0.5>tap_position):
                    optimial_tap_position = (self.PowerSimModel.grid_data['transformer']['tap_max'])+i
        elif(self.PowerSimModel.grid_data['transformer']['tap_max'] > self.PowerSimModel.grid_data['transformer']['tap_min']):
            for i in range(number_of_taps_max_min[0]):
                if((self.PowerSimModel.grid_data['transformer']['tap_max'])+i-0.5<tap_position and (self.PowerSimModel.grid_data['transformer']['tap_max'])+i+0.5>tap_position):
                    optimial_tap_position = (self.PowerSimModel.grid_data['transformer']['tap_min'])+i

        return optimial_tap_position
