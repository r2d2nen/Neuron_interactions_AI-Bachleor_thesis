from parameters import Parameters
from nsoptcaller import NsoptCaller
from gaussfit import Gaussfit
from datamanager import Datamanager
import numpy as np


#### BE CERTAIN TO SET THE TAGS AND WHICH LEC GENERATING METHOD YOU WANT TO USE!

#Do we want to generate new samples? And if so, how many? SET TAGS 
generate_data = True
process_data = False
samples = 1000
generate_tags = ['sgt50', 'validation' + str(samples), 'D_center_100%_random_uniform_lecs']
training_tags = ['sgt50', 'training1000', 'D_center_100%']
validation_tags = ['sgt50', 'validation1000', 'D_center_100%']
lec_lhs = False   # Set True for random uniform lecs
LEC_LENGTH = 16
energy = 50

# Set up necessary classes)
param = Parameters(1, samples, center_lecs='center_of_interval')
nsopt = NsoptCaller()
gauss = Gaussfit()
dm = Datamanager(echo=False)



# Sample generation, add to database. Do we want to generate and are the tags not used before?
# TODO(DANIEL): Add question if used really wants to add data to tags already used
#for samples in xrange(200, 1600, 100):
    

if generate_data and dm.num_matches(generate_tags) <= 0:
    print('hej')
    param.nbr_of_samples = samples
    if lec_lhs:
        lecs = param.create_lhs_lecs()
    else:
        lecs = param.create_random_uniform_lecs()
    
    print('THIS IS SHIT: %r %r %r') % (samples, generate_tags, lecs)
    print('Getting observables')
    observables = nsopt.get_nsopt_observable(lecs)
    print('Inserting data')
    for i in xrange(samples):
        dm.insert(tags=generate_tags, observable=observables[i][0], energy=energy, LECs=lecs[i])
    
    #for row in dm.read(['test']):
        #print row.observable
        #print(param.create_monospaced_lecs())
        #print(param.create_lhs_lecs())
            
if process_data:
    #Set empty arrays with zeros for training and validation data
    train_obs = np.array([0])
    train_energy = np.array([0])
    train_lecs = np.array(np.zeros(LEC_LENGTH))

    #Read database data with the specified tags
    for row in dm.read(training_tags):
        train_obs = np.vstack((train_obs, row.observable))
        train_energy = np.vstack((train_energy, row.energy))
        train_lecs = np.vstack((train_lecs, row.LECs))

    # Clean up initialized zeros
    train_obs = np.delete(train_obs, 0, 0)
    train_energy = np.delete(train_energy, 0, 0)
    train_lecs = np.delete(train_lecs, 0, 0)

    # Set up Gaussfit stuff and plot our model error
    gauss.set_gp_kernel(in_dim=LEC_LENGTH)
    #train_lecs = gauss.rescale(train_lecs)
    gauss.populate_gp_model(train_obs, train_lecs)
    gauss.optimize()
    
    for sample in xrange(100, 200, 100):
        val_obs = np.array([0])
        val_energy = np.array([0])
        val_lecs = np.array(np.zeros(LEC_LENGTH))
        #validation_tags[1] = 'validation' + str(sample)
        for row in dm.read(validation_tags):
            val_obs = np.vstack((val_obs, row.observable))
            val_energy = np.vstack((val_energy, row.energy))
            val_lecs = np.vstack((val_lecs, row.LECs))

                
        val_obs = np.delete(val_obs, 0, 0)
        val_energy = np.delete(val_energy, 0, 0)
        val_lecs = np.delete(val_lecs, 0,0)
        val_lecs = gauss.rescale(val_lecs)
        gauss.plot_predicted_actual(val_lecs, val_obs)
        print gauss.get_sigma_intervals(val_lecs, val_obs)
        gauss.plot_modelerror(val_lecs, train_lecs, val_obs)
        print('Number of validation data: ' + str(sample))
        print('Model error: ' + str(gauss.get_model_error(val_lecs, val_obs)))

