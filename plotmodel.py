import numpy as np
from scipy.spatial.distance import cdist
from matplotlib import pyplot as plt

# Xvalid
# Xlearn
# Yvalid
# Ymodel
Xvalid = np.array(
[[ 0, 0 ],
 [ 0, 3]])
Xlearn = np.array(
[[ 0, 0 ],
 [ 1, 2],
 [ 0, 4]])


alldists = cdist( Xvalid, Xlearn, "euclidean" )

mindists = np.min( alldists, axis=1)

plt.plot( mindists, Ymodel-Yvalid )

plt.show()


print alldists
print mindists
