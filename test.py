from parameters import Parameters
from nsoptcaller import NsoptCaller
from gaussfit import Gaussfit
from datamanager import Datamanager
import numpy as np

samples = 50

param = Parameters(0.1, samples)
nsopt = NsoptCaller()
gauss = Gaussfit()
dm = Datamanager(echo=False)

nsopt.X = 50
train_obs = np.array([0])
train_energy = np.array([0])
train_lecs = np.array(np.zeros(16))

val_obs = np.array([0])
val_energy = np.array([0])
val_lecs = np.array(np.zeros(16))
for row in dm.read(['sgt', 'training']):
    train_obs = np.vstack((train_obs, row.observable))
    train_energy = np.vstack((train_energy, row.energy))
    train_lecs = np.vstack((train_lecs, row.LECs))
for row in dm.read(['sgt', 'validation']):
    val_obs = np.vstack((val_obs, row.observable))
    val_energy = np.vstack((val_energy, row.energy))
    val_lecs = np.vstack((val_lecs, row.LECs))

train_obs = np.delete(train_obs, 0, 0)
train_energy = np.delete(train_energy, 0, 0)
train_lecs = np.delete(train_lecs, 0, 0)

val_obs = np.delete(val_obs, 0, 0)
val_energy = np.delete(val_energy, 0, 0)
val_lecs = np.delete(val_lecs, 0, 0)
print(train_obs)
print(train_lecs)
gauss.set_gp_kernel(in_dim=16)
gauss.populate_gp_model(train_obs, train_lecs)


gauss.optimize()

gauss.plot()

print (val_obs)
    
    

