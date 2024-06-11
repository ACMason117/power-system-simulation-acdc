import graph_processing as gp
import power_flow_processing as pfp

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

    def optimal_tap_position():
        pass
