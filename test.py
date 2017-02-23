from parameters import Parameters
import numpy as np

param = Parameters(0.1, 1)
print(param.center_of_lecs_interval())
print(param.create_monospaced_lecs())
print(param.create_lhs_lecs())
