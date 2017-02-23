from parameters import Parameters
import numpy as np

param = Parameters(0.1, 50)

print(param.create_monospaced_lecs())
print(param.create_lhs_lecs())

zero = np.zeros((5,5))
ones = np.ones(5)
#print(zero)
#print(ones)

#print(zero+ones)
