from parameters import Parameters
from nsoptcaller import NsoptCaller
from gaussfit import Gaussfit
from datamanager import Datamanager
import numpy as np

#Do we want to generate new samples? And if so, how many? SET TAGS 
generate_data = False
process_data = True
samples = 50
generate_tags = ['sgt',]
training_tags = ['sgt', 'training']
validation_tags = ['sgt', 'validation']
LEC_LENGTH = 16
energies = 50

# Set up necessary classes)
param = Parameters(0.1, samples)
nsopt = NsoptCaller()
gauss = Gaussfit()
dm = Datamanager(echo=False)



# Sample generation, add to database, be sure to set tags before doing this.
if generate_data:
    lecs = param.create_lhs_lecs()
    observables = nsopt.get_nsopt_observable(lecs)
    for i in range(samples):
        dm.insert(tags=generate_tags, observable=observables[i][0], energy=50, LECs=lecs[i])
        
    #for row in dm.read(['test']):
        #print row.observable
        #print(param.create_monospaced_lecs())
        #print(param.create_lhs_lecs())
            



if process_data:
    nsopt.X = 50

    #Set empty arrays with zeros for training and validation data
    train_obs = np.array([0])
    train_energy = np.array([0])
    train_lecs = np.array(np.zeros(LEC_LENGTH))

    val_obs = np.array([0])
    val_energy = np.array([0])
    val_lecs = np.array(np.zeros(LEC_LENGTH))

    #Read database data with the specified tags
    for row in dm.read(training_tags):
        train_obs = np.vstack((train_obs, row.observable))
        train_energy = np.vstack((train_energy, row.energy))
        train_lecs = np.vstack((train_lecs, row.LECs))
    for row in dm.read(validation_tags):
        val_obs = np.vstack((val_obs, row.observable))
        val_energy = np.vstack((val_energy, row.energy))
        val_lecs = np.vstack((val_lecs, row.LECs))

    # Clean up initialized zeros
    train_obs = np.delete(train_obs, 0, 0)
    train_energy = np.delete(train_energy, 0, 0)
    train_lecs = np.delete(train_lecs, 0, 0)

    val_obs = np.delete(val_obs, 0, 0)
    val_energy = np.delete(val_energy, 0, 0)
    val_lecs = np.delete(val_lecs, 0, 0)


    # Set up Gaussfit stuff and plot our model error
    gauss.set_gp_kernel(in_dim=LEC_LENGTH)
    gauss.populate_gp_model(train_obs, train_lecs)
    gauss.optimize()
    gauss.plot_modelerror(val_lecs, train_lecs, val_obs)
    gauss.plot_model(val_lecs, train_lecs, val_obs)
    

    

